#!/usr/bin/env python3
"""Test script for the Script Generation API."""

import asyncio
import sys
from app.models.script import ScriptGenerationRequest
from app.services.script_orchestrator import get_orchestrator


async def test_without_api_keys():
    """Test basic structure without API keys."""
    print("\n🧪 Testing Script Generation Service Structure...\n")
    
    # Create test request
    request = ScriptGenerationRequest(
        title="Test Video",
        description="A simple test video about Python programming",
        use_case="educational",
        language="en",
        style="professional",
        duration=30,
        nb_section=1,
        regenerer_script=False,
        script_text="This is a test script about Python programming basics."
    )
    
    print("✅ Request model validated successfully")
    print(f"   - Title: {request.title}")
    print(f"   - Use Case: {request.use_case}")
    print(f"   - Language: {request.language}")
    print(f"   - Duration: {request.duration}s")
    print(f"   - Sections: {request.nb_section}")
    
    # Check orchestrator initialization
    orchestrator = get_orchestrator()
    print("\n✅ Orchestrator initialized successfully")
    print(f"   - Title Agent: {orchestrator.title_agent.__class__.__name__}")
    print(f"   - Sections Agent: {orchestrator.sections_agent.__class__.__name__}")
    print(f"   - Description Agent: {orchestrator.description_agent.__class__.__name__}")
    print(f"   - Keywords Agent: {orchestrator.keywords_agent.__class__.__name__}")
    print(f"   - Transcription Service: {orchestrator.transcription_service.__class__.__name__}")
    
    print("\n✅ All components loaded successfully!")
    print("\n⚠️  To test full generation, please configure:")
    print("   1. DEEPSEEK_API_KEY in .env")
    print("   2. ASSEMBLYAI_API_KEY in .env")
    
    return True


async def test_with_api_keys():
    """Test full generation with API keys (if available)."""
    from app.core.llm_client import get_llm_client
    from app.services.transcription_service import get_transcription_service
    
    llm_client = get_llm_client()
    transcription_service = get_transcription_service()
    
    if not llm_client.is_available():
        print("\n⚠️  LLM client not available. Please set DEEPSEEK_API_KEY in .env")
        return False
    
    if not transcription_service.client:
        print("\n⚠️  Transcription service not available. Please set ASSEMBLYAI_API_KEY in .env")
    
    print("\n🚀 Testing full script generation...\n")
    
    request = ScriptGenerationRequest(
        title="Quick Python Tip",
        description="Learn Python list comprehension in 30 seconds",
        use_case="youtube_short",
        language="en",
        style="casual",
        duration=30,
        nb_section=1
    )
    
    orchestrator = get_orchestrator()
    response = await orchestrator.generate_script(request)
    
    print("✅ Script generated successfully!\n")
    print(f"📝 Title: {response.title}")
    print(f"📄 Script ({len(response.script_text)} chars):")
    print(f"   {response.script_text[:200]}...")
    print(f"\n🔑 Keywords: {response.keywords}")
    print(f"\n📋 Description ({len(response.video_description)} chars):")
    print(f"   {response.video_description[:200]}...")
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("   Script Generation Service - Test Suite")
    print("=" * 60)
    
    try:
        # Test structure first
        asyncio.run(test_without_api_keys())
        
        # Try full test if keys are available
        print("\n" + "=" * 60)
        print("   Attempting Full Generation Test")
        print("=" * 60)
        asyncio.run(test_with_api_keys())
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("   Tests Completed")
    print("=" * 60)
