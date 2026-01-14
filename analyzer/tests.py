"""
Tests for AI Job Matcher application.
"""
import pytest
from django.test import Client
from unittest.mock import Mock, patch
from analyzer.services.cv_parser import CVParserService
from analyzer.services.firebase_auth import FirebaseAuthService
from analyzer.services.llm_client import LLMClientService


class TestCVParser:
    """Test CV parsing functionality."""
    
    def test_validate_file_size_exceeds_limit(self):
        """Test that oversized files are rejected."""
        mock_file = Mock()
        mock_file.size = 10 * 1024 * 1024  # 10MB
        
        with pytest.raises(ValueError, match="exceeds maximum"):
            CVParserService.validate_file(mock_file, "test.pdf")
    
    def test_validate_file_invalid_extension(self):
        """Test that invalid file types are rejected."""
        mock_file = Mock()
        mock_file.size = 1024
        
        with pytest.raises(ValueError, match="not supported"):
            CVParserService.validate_file(mock_file, "test.txt")


class TestLLMClient:
    """Test LLM client functionality."""
    
    def test_parse_response_with_json(self):
        """Test parsing valid JSON response."""
        json_content = '{"match_score": 75, "strengths": ["A"], "missing_skills": ["B"], "improvement_suggestions": ["C"], "summary": "Good"}'
        
        result = LLMClientService._parse_response(json_content)
        
        assert result['match_score'] == 75
        assert len(result['strengths']) == 1
    
    def test_validate_result_missing_field(self):
        """Test validation fails for missing required fields."""
        invalid_result = {
            'match_score': 75,
            'strengths': ['A']
            # Missing other required fields
        }
        
        with pytest.raises(ValueError, match="Missing required field"):
            LLMClientService._validate_result(invalid_result)
    
    def test_validate_result_invalid_score_range(self):
        """Test validation fails for out-of-range score."""
        invalid_result = {
            'match_score': 150,  # Invalid
            'strengths': ['A'],
            'missing_skills': ['B'],
            'improvement_suggestions': ['C'],
            'summary': 'Test'
        }
        
        with pytest.raises(ValueError, match="must be between 0-100"):
            LLMClientService._validate_result(invalid_result)


@pytest.mark.django_db
class TestViews:
    """Test Django views."""
    
    def test_home_page_loads(self):
        """Test that home page loads successfully."""
        client = Client()
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'AI Job Matcher' in response.content
    
    def test_analyze_without_auth_fails(self):
        """Test that analyze endpoint requires authentication."""
        client = Client()
        response = client.post('/analyze/')
        
        assert response.status_code == 401
