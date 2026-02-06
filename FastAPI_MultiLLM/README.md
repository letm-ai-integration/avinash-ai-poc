# Multi-Model LLM Inference API (FastAPI)

This application provides a **FastAPI-based REST API** that allows users to interact with multiple Large Language Models (LLMs) hosted on **Hugging Face** and **Groq**. Users can query available models and submit prompts to any supported model to receive responses.

## Overview

The application exposes API endpoints that:
- List all available LLM models
- Accept user queries along with a selected model
- Forward requests to the corresponding provider (Hugging Face or Groq)
- Return generated responses from the selected model

This design enables flexible, provider-agnostic access to multiple LLMs through a single API interface.

## Architecture

The application follows a simple request–response flow:

1. **Client Request**
   - User queries available models or submits a prompt with a selected model

2. **FastAPI Backend**
   - Validates input
   - Routes the request to the appropriate model provider

3. **Model Providers**
   - **Hugging Face**: Hosted open-source and proprietary models
   - **Groq**: High-performance inference for supported LLMs

4. **Response Handling**
   - Model output is returned to the user in a standardized API response

