"""
LLM Client Service
Integrates with OpenAI-compatible LLM API for CV-Job matching analysis.
"""
import json
import logging
from typing import Dict, Any, Optional

import openai
from django.conf import settings

logger = logging.getLogger(__name__)


class LLMClientService:
    """
    Service for interacting with OpenAI-compatible LLM APIs.
    Performs structured CV-to-job-description analysis with JSON output.
    """
    
    # System prompt for structured analysis
    SYSTEM_PROMPT = """You are an elite HR analyst, ATS expert, and career strategist with 20+ years of experience in talent acquisition across Fortune 500 companies. Your task is to perform a comprehensive, forensic-level analysis of how well a candidate's CV matches a given job description.

You must respond ONLY with valid JSON in this exact format.
CRITICAL JSON RULES:
- Output must be valid JSON (RFC 8259). No markdown. No extra keys.
- Do NOT include literal newline characters inside any JSON string values. If you need line breaks, encode them as the two characters "\\n".
- Avoid unescaped double quotes inside strings.
- Keep the response concise enough to fit within the output token limit. If you are running out of space, shorten detailed_narrative first.
- detailed_narrative must be concise (3-5 paragraphs). Each paragraph should be 1-2 sentences.

Format:
{
  "match_score": <number between 0-100>,
  "ats_compatibility_score": <number between 0-100>,
  "executive_summary": "<3-4 sentence high-level assessment suitable for a hiring manager>",
  "strengths": [
    {"point": "<strength>", "evidence": "<specific evidence from CV>", "impact": "<why this matters for the role>"}
  ],
  "critical_gaps": [
    {"gap": "<missing requirement>", "importance": "critical|high|medium", "recommendation": "<how to address>"}
  ],
  "skill_analysis": {
    "matched_hard_skills": ["<list of technical skills that match>"],
    "matched_soft_skills": ["<list of soft skills that match>"],
    "missing_hard_skills": ["<technical skills not found>"],
    "missing_soft_skills": ["<soft skills not found>"],
    "transferable_skills": ["<skills that could transfer>"]
  },
  "experience_fit": {
    "years_required": "<from job description or 'Not specified'>",
    "years_apparent": "<estimated from CV>",
    "relevance_score": <0-100>,
    "industry_alignment": "<assessment of industry experience match>"
  },
  "education_fit": {
    "meets_requirements": true|false,
    "details": "<assessment of educational qualifications>"
  },
  "red_flags": ["<any concerns a recruiter might have>"],
  "competitive_advantages": ["<what makes this candidate stand out>"],
  "interview_questions": ["<3-5 questions a recruiter should ask based on gaps>"],
  "cv_improvement_tips": [
    {"tip": "<actionable suggestion>", "priority": "high|medium|low", "expected_impact": "<how this improves match>"}
  ],
  "salary_negotiation_position": "<strong|moderate|weak based on match>",
  "final_recommendation": "<STRONG MATCH|GOOD MATCH|CONDITIONAL MATCH|WEAK MATCH|NOT RECOMMENDED>",
    "detailed_narrative": [
        "<paragraph 1 (1-2 sentences, single line)>",
        "<paragraph 2 (1-2 sentences, single line)>",
        "<paragraph 3 (1-2 sentences, single line)>"
    ]
}

Analysis Guidelines:
- match_score: 0-30 (poor), 31-50 (below average), 51-70 (average), 71-85 (good), 86-100 (excellent)
- Be brutally honest but constructive - candidates need truth to improve
- Analyze keyword density and ATS optimization
- Consider career progression and trajectory
- Evaluate cultural fit signals if present
- Look for quantifiable achievements (numbers, percentages, dollar amounts)
- Assess leadership and management experience if relevant
- Check for industry-specific certifications and tools
- Identify any employment gaps or job-hopping patterns
- Consider the seniority level match

The detailed_narrative should read like a professional recruiter's assessment report (3-5 short paragraphs; each paragraph must be a single line string with no literal newlines).

Do not include any text outside the JSON structure. No markdown wrappers, no explanations, just valid JSON."""
    
    @classmethod
    def _create_user_prompt(cls, cv_text: str, job_description: str) -> str:
        """
        Create the user prompt combining CV and job description.
        
        Args:
            cv_text: Extracted text from CV
            job_description: Job description provided by user
            
        Returns:
            Formatted user prompt
        """
        return f"""Please analyze the following CV against the job description:

JOB DESCRIPTION:
{job_description}

CANDIDATE CV:
{cv_text}

Provide your analysis in the required JSON format."""
    
    @classmethod
    def analyze(cls, cv_text: str, job_description: str) -> Dict[str, Any]:
        """
        Perform CV-to-job analysis using LLM.
        
        Args:
            cv_text: Extracted text from the candidate's CV
            job_description: Job description to match against
            
        Returns:
            dict containing:
                - match_score: int (0-100)
                - strengths: list of strings
                - missing_skills: list of strings
                - improvement_suggestions: list of strings
                - summary: string
                
        Raises:
            ValueError: If LLM response is invalid or cannot be parsed
            Exception: If API call fails
        """
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        
        try:
            # Create user prompt
            user_prompt = cls._create_user_prompt(cv_text, job_description)

            logger.info(f"Sending analysis request to LLM (model: {settings.OPENAI_MODEL})")

            content = cls._call_llm(user_prompt)

            logger.info("Received response from LLM")
            logger.debug(f"Raw response: {content[:200]}...")

            try:
                result = cls._parse_response(content)
            except json.JSONDecodeError as e:
                logger.warning(f"LLM returned invalid JSON ({e}); retrying once with stricter instructions")
                strict_user_prompt = (
                    user_prompt
                    + "\n\nCRITICAL: Return STRICT valid JSON only. "
                      "No markdown. No extra text. No literal newlines inside strings (use \\\\n). "
                        "The 'detailed_narrative' field must be an array of single-line strings. "
                        "Return the entire JSON on ONE LINE (minified), with no line breaks."
                )
                # Lower temperature and cap tokens on retry to reduce likelihood of truncation/format drift.
                retry_max_tokens = min(getattr(settings, "OPENAI_MAX_TOKENS", 2000), 2000)
                content = cls._call_llm(strict_user_prompt, temperature=0.0, max_tokens=retry_max_tokens)
                result = cls._parse_response(content)

            # Validate result structure
            cls._validate_result(result)

            logger.info("Successfully parsed and validated LLM response")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError(f"LLM returned invalid JSON: {str(e)}")

        except Exception as e:
            # Normalize OpenAI SDK v1 exceptions without depending on openai.error (removed in v1)
            auth_exc = getattr(openai, "AuthenticationError", None)
            rate_exc = getattr(openai, "RateLimitError", None)
            api_exc = getattr(openai, "APIError", None)
            bad_req_exc = getattr(openai, "BadRequestError", None)

            if auth_exc and isinstance(e, auth_exc):
                logger.error("OpenAI authentication failed")
                raise ValueError("LLM API authentication failed. Please check API key.")
            if rate_exc and isinstance(e, rate_exc):
                logger.error("OpenAI rate limit exceeded")
                raise ValueError("LLM API rate limit exceeded. Please try again later.")
            if bad_req_exc and isinstance(e, bad_req_exc):
                logger.error(f"OpenAI bad request: {e}")
                raise ValueError(f"LLM request rejected: {str(e)}")
            if api_exc and isinstance(e, api_exc):
                logger.error(f"OpenAI API error: {e}")
                raise ValueError(f"LLM API error: {str(e)}")

            logger.exception(f"Unexpected error during LLM analysis: {e}")
            raise

    @classmethod
    def _call_llm(
        cls,
        user_prompt: str,
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Call the configured OpenAI-compatible endpoint and return raw text content."""
        messages = [
            {"role": "system", "content": cls.SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        use_temperature = settings.OPENAI_TEMPERATURE if temperature is None else temperature
        use_max_tokens = settings.OPENAI_MAX_TOKENS if max_tokens is None else max_tokens

        # Prefer OpenAI Python SDK v1 client if available.
        if hasattr(openai, "OpenAI"):
            client = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_API_BASE,
            )

            # response_format is supported by OpenAI for JSON mode; some proxies/providers may reject it.
            try:
                resp = client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=messages,
                    temperature=use_temperature,
                    max_tokens=use_max_tokens,
                    response_format={"type": "json_object"},
                )
            except Exception as e:
                bad_req_exc = getattr(openai, "BadRequestError", None)
                if bad_req_exc and isinstance(e, bad_req_exc):
                    logger.info("response_format rejected by provider; retrying without it")
                    resp = client.chat.completions.create(
                        model=settings.OPENAI_MODEL,
                        messages=messages,
                        temperature=use_temperature,
                        max_tokens=use_max_tokens,
                    )
                else:
                    raise

            content = resp.choices[0].message.content
            if not content:
                raise ValueError("LLM returned empty response")
            return content.strip()

        # Legacy fallback (OpenAI python < 1.0)
        openai.api_key = settings.OPENAI_API_KEY
        openai.api_base = settings.OPENAI_API_BASE

        api_params = {
            "model": settings.OPENAI_MODEL,
            "messages": messages,
            "temperature": use_temperature,
            "max_tokens": use_max_tokens,
        }

        try:
            resp = openai.ChatCompletion.create(**api_params, response_format={"type": "json_object"})
        except TypeError:
            logger.info("response_format not supported; retrying without it")
            resp = openai.ChatCompletion.create(**api_params)

        content = resp.choices[0].message.content
        if not content:
            raise ValueError("LLM returned empty response")
        return content.strip()
    
    @staticmethod
    def _parse_response(content: str) -> Dict[str, Any]:
        """
        Parse LLM response content into structured dict.
        
        Args:
            content: Raw response content from LLM
            
        Returns:
            Parsed dictionary
            
        Raises:
            json.JSONDecodeError: If content is not valid JSON
        """
        # Try to extract JSON if wrapped in markdown code blocks
        if '```json' in content:
            start = content.find('```json') + 7
            end = content.find('```', start)
            content = content[start:end].strip()
        elif '```' in content:
            start = content.find('```') + 3
            end = content.find('```', start)
            content = content[start:end].strip()
        
        # First attempt: direct parse
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        # Second attempt: extract first JSON object in the text
        start_obj = content.find('{')
        end_obj = content.rfind('}')
        if start_obj == -1 or end_obj == -1 or end_obj <= start_obj:
            # Likely truncated or surrounded by extra text.
            raise json.JSONDecodeError("Truncated or missing JSON object", content, max(start_obj, 0))

        candidate = content[start_obj:end_obj + 1]

        # Third attempt: repair common JSON issues produced by LLMs
        repaired = LLMClientService._repair_common_json_issues(candidate)

        return json.loads(repaired)

    @staticmethod
    def _repair_common_json_issues(raw: str) -> str:
        """Attempt to repair common JSON issues produced by LLMs.

        Repairs:
        - Escapes literal newlines/carriage returns inside JSON strings.
        - Escapes unescaped double-quotes inside JSON strings when they don't appear to terminate the string.
        """
        out_chars: list[str] = []
        in_string = False
        escape_next = False

        def _next_non_ws(s: str, start: int) -> str:
            i = start
            while i < len(s) and s[i] in (' ', '\t', '\n', '\r'):
                i += 1
            return s[i] if i < len(s) else ''

        i = 0
        while i < len(raw):
            ch = raw[i]

            if escape_next:
                out_chars.append(ch)
                escape_next = False
                i += 1
                continue

            if ch == '\\':
                out_chars.append(ch)
                escape_next = True
                i += 1
                continue

            if ch == '"':
                if not in_string:
                    in_string = True
                    out_chars.append(ch)
                    i += 1
                    continue

                # We are inside a string; decide whether this quote terminates the string
                nxt = _next_non_ws(raw, i + 1)
                # After a closing quote in valid JSON, we expect one of: colon (key), comma/end braces (value)
                if nxt in (':', ',', '}', ']', ''):
                    in_string = False
                    out_chars.append(ch)
                else:
                    # Likely an unescaped quote inside the string; escape it.
                    out_chars.append('\\"')
                i += 1
                continue

            if in_string and ch == '\n':
                out_chars.append('\\n')
                i += 1
                continue
            if in_string and ch == '\r':
                out_chars.append('\\r')
                i += 1
                continue

            out_chars.append(ch)
            i += 1

        return ''.join(out_chars)
    
    @staticmethod
    def _validate_result(result: Dict[str, Any]) -> None:
        """
        Validate that result has required fields and correct types.
        
        Args:
            result: Parsed result dictionary
            
        Raises:
            ValueError: If validation fails
        """
        # Core required fields
        required_fields = {
            'match_score': (int, float),
            'executive_summary': str,
            'strengths': list,
            'critical_gaps': list,
            'final_recommendation': str,
            'detailed_narrative': (str, list)
        }
        
        for field, expected_type in required_fields.items():
            if field not in result:
                raise ValueError(f"Missing required field: {field}")
            
            if not isinstance(result[field], expected_type):
                raise ValueError(
                    f"Field '{field}' has incorrect type. "
                    f"Expected {expected_type}, got {type(result[field])}"
                )
        
        # Validate match_score range
        score = result['match_score']
        if not (0 <= score <= 100):
            raise ValueError(f"match_score must be between 0-100, got {score}")
        
        # Ensure strengths list is not empty - add default if needed
        if not result['strengths']:
            logger.warning("LLM returned empty strengths list; adding default")
            result['strengths'] = [
                {
                    "point": "CV provided",
                    "evidence": "Candidate submitted a CV for consideration",
                    "impact": "Establishes baseline for further review"
                }
            ]
        
        # Ensure critical_gaps is not empty - add default if needed
        if not result.get('critical_gaps'):
            logger.warning("LLM returned empty critical_gaps list; adding default")
            result['critical_gaps'] = [
                {
                    "gap": "Insufficient CV content",
                    "importance": "high",
                    "recommendation": "Please provide a more detailed CV"
                }
            ]
        
        # Validate summary is not empty
        if not result['executive_summary'].strip():
            raise ValueError("Executive summary cannot be empty")
        
        # Ensure detailed_narrative exists and is formatted correctly
        if not result.get('detailed_narrative'):
            logger.warning("LLM returned empty detailed_narrative; adding default")
            result['detailed_narrative'] = [
                "Limited CV information available for assessment.",
                "Recommend providing additional details for accurate matching.",
                "Follow up with candidate for more comprehensive profile information."
            ]
