# AURALFLOW AI - Folder Structure

```
video-dubbing-platform/
│
├── frontend/                          # Next.js frontend application
│   ├── public/                        # Static assets
│   │   ├── locales/                   # Internationalization files
│   │   └── assets/                    # Images, icons, etc.
│   ├── src/
│   │   ├── app/                       # Next.js app router pages
│   │   │   ├── (auth)/                # Authentication routes
│   │   │   │   ├── login/
│   │   │   │   ├── register/
│   │   │   │   └── forgot-password/
│   │   │   ├── dashboard/             # User dashboard
│   │   │   ├── projects/              # Project management
│   │   │   └── api/                   # Frontend API routes
│   │   ├── components/                # Reusable UI components
│   │   │   ├── ui/                    # ShadCN UI components
│   │   │   ├── forms/                 # Form components
│   │   │   ├── layout/                # Layout components
│   │   │   └── video/                 # Video-specific components
│   │   ├── hooks/                     # Custom React hooks
│   │   ├── lib/                       # Utility functions
│   │   │   ├── api/                   # API client
│   │   │   └── auth/                  # Auth utilities
│   │   ├── providers/                 # Context providers
│   │   ├── styles/                    # Global styles
│   │   └── types/                     # TypeScript type definitions
│   ├── .env.local                     # Environment variables (local)
│   ├── .env.production                # Environment variables (production)
│   ├── next.config.js                 # Next.js configuration
│   ├── tailwind.config.js             # Tailwind CSS configuration
│   ├── tsconfig.json                  # TypeScript configuration
│   └── package.json                   # Frontend dependencies
│
├── backend/                           # FastAPI backend application
│   ├── app/
│   │   ├── api/                       # API endpoints
│   │   │   ├── routes/
│   │   │   │   ├── auth.py            # Auth endpoints
│   │   │   │   ├── videos.py          # Video processing endpoints
│   │   │   │   ├── users.py           # User management endpoints
│   │   │   │   └── voice.py           # Voice cloning endpoints
│   │   │   ├── dependencies.py        # FastAPI dependencies
│   │   │   └── middlewares.py         # API middlewares
│   │   ├── core/                      # Core app functionality
│   │   │   ├── config.py              # App configuration
│   │   │   ├── security.py            # Security utilities
│   │   │   └── events.py              # App events (startup, shutdown)
│   │   ├── db/                        # Database module
│   │   │   ├── models/                # SQLAlchemy models
│   │   │   ├── repositories/          # Data access layer
│   │   │   ├── migrations/            # Alembic migrations
│   │   │   └── session.py             # Database session
│   │   ├── schemas/                   # Pydantic schemas
│   │   │   ├── requests/              # Request schemas
│   │   │   └── responses/             # Response schemas
│   │   ├── services/                  # Business logic
│   │   │   ├── auth_service.py        # Authentication service
│   │   │   ├── video_service.py       # Video processing service
│   │   │   └── voice_service.py       # Voice cloning service
│   │   └── utils/                     # Utility functions
│   ├── workers/                       # Celery workers
│   │   ├── tasks/                     # Celery tasks
│   │   │   ├── audio_tasks.py         # Audio processing tasks
│   │   │   ├── video_tasks.py         # Video processing tasks
│   │   │   └── ml_tasks.py            # ML processing tasks
│   │   ├── celery_app.py              # Celery configuration
│   │   └── worker.py                  # Worker entry point
│   ├── tests/                         # Backend tests
│   │   ├── conftest.py                # Test configuration
│   │   ├── api/                       # API tests
│   │   ├── services/                  # Service tests
│   │   └── workers/                   # Worker tests
│   ├── alembic.ini                    # Alembic configuration
│   ├── pyproject.toml                 # Project metadata
│   ├── poetry.lock                    # Dependency lock file
│   ├── .env                           # Environment variables
│   └── main.py                        # Application entry point
│
├── ml/                                # Machine learning module
│   ├── models/                        # ML model definitions
│   │   ├── whisper/                   # Speech recognition model
│   │   ├── demucs/                    # Voice separation model
│   │   ├── xttsvs2/                   # Text-to-speech model
│   │   ├── nllb/                      # Translation model
│   │   └── wav2lip/                   # Lip syncing model (optional)
│   ├── pipelines/                     # ML pipelines
│   │   ├── transcription.py           # Transcription pipeline
│   │   ├── translation.py             # Translation pipeline
│   │   ├── voice_cloning.py           # Voice cloning pipeline
│   │   └── vocal_separation.py        # Vocal separation pipeline
│   ├── preprocessing/                 # Data preprocessing utilities
│   ├── training/                      # Model training scripts
│   ├── inference/                     # Model inference scripts
│   └── utils/                         # ML utility functions
│
├── infrastructure/                    # Infrastructure configuration
│   ├── docker/                        # Docker configuration
│   │   ├── frontend/                  # Frontend Dockerfile
│   │   ├── backend/                   # Backend Dockerfile
│   │   ├── ml/                        # ML Dockerfile
│   │   └── docker-compose.yml         # Docker Compose configuration
│   ├── k8s/                           # Kubernetes configuration (if needed)
│   ├── terraform/                     # Infrastructure as Code
│   └── nginx/                         # Nginx configuration
│
├── scripts/                           # Utility scripts
│   ├── setup.sh                       # Setup script
│   ├── deploy.sh                      # Deployment script
│   └── seed_db.py                     # Database seeding script
│
├── storage/                           # Local storage (during development)
│   ├── uploads/                       # Uploaded files
│   ├── processed/                     # Processed files
│   └── .gitignore                     # Ignore storage contents
│
├── docs/                              # Documentation
│   ├── api/                           # API documentation
│   ├── architecture/                  # Architecture documentation
│   ├── deployment/                    # Deployment guides
│   └── development/                   # Development guides
│
├── .github/                           # GitHub configuration
│   └── workflows/                     # GitHub Actions workflows
│       ├── backend-ci.yml             # Backend CI workflow
│       ├── frontend-ci.yml            # Frontend CI workflow
│       └── deploy.yml                 # Deployment workflow
│
├── .gitignore                         # Git ignore file
├── .env.example                       # Example environment variables
├── docker-compose.yml                 # Root Docker Compose (dev environment)
├── docker-compose.prod.yml            # Production Docker Compose
├── README.md                          # Project readme
└── LICENSE                            # Project license
```

# Voice Dubbing & Cloning Backend Setup Guide

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Redis (Required for Celery)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

**macOS:**
```bash
brew install redis
brew services start redis
```

**Windows:**
```bash
# Using WSL or Docker
docker run -d -p 6379:6379 --name redis redis:alpine
```

### 3. Create Required Directories

```bash
mkdir -p backend/uploads/voice/output
mkdir -p backend/logs
```

### 4. Environment Configuration

Create `backend/.env`:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Celery Configuration
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# File Upload Configuration
MAX_FILE_SIZE=104857600  # 100MB in bytes
UPLOAD_DIR=uploads

# ML Model Configuration
MODELS_DIR=ml/models
WHISPER_MODEL=base
NLLB_MODEL=facebook/nllb-200-distilled-600M
```

## Running the Application

### 1. go to backend directory
```bash
cd backend
```

### 2. Start Redis Server
```bash
redis-server
```
### 3. create a vertual environment
```bash
python3 -m venv venv
```
### 4. activate the virtual environment:
```bash
source venv/bin/activate
```

### 5. Start Celery Worker
```bash
cd backend
celery -A workers.celery_app worker --loglevel=info
```

### 3. Start FastAPI Server
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Optional: Start Celery Flower (Monitoring)
```bash
celery -A workers.celery_app flower --port=5555
```

## API Endpoints

### Voice Cloning Endpoints

1. **Submit Voice Clone Request**
   - `POST /api/voice/voice-clone`
   - Accepts file upload or URL link
   - Returns task ID for tracking

2. **Check Task Status**
   - `GET /api/voice/status/{task_id}`
   - Returns current processing status

3. **Cancel Task**
   - `DELETE /api/voice/task/{task_id}`
   - Cancels running task

4. **Get Supported Formats**
   - `GET /api/voice/supported-formats`
   - Returns supported file formats and languages

## Frontend Integration

Update your Next.js environment variables in `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Testing the API

### Using curl:

```bash
# Upload a file
curl -X POST "http://localhost:8000/api/voice/voice-clone" \
  -F "type=file" \
  -F "file=@sample.mp3" \
  -F "target_language=es" \
  -F "source=local"

# Check status
curl "http://localhost:8000/api/voice/status/your-task-id"

# Submit URL
curl -X POST "http://localhost:8000/api/voice/voice-clone" \
  -F "type=link" \
  -F "link=https://example.com/audio.mp3" \
  -F "target_language=fr" \
  -F "source=youtube"
```

## Integrating Your ML Pipelines

Replace the placeholder functions in `audio_tasks.py` with your actual ML pipeline calls:

```python
# Replace these imports with your actual pipelines
from ml.pipelines.transcription import transcribe_audio
from ml.pipelines.translation import translate_text
from ml.pipelines.vocal_separation import separate_vocals
from ml.pipelines.voice_cloning import clone_voice
```

## Monitoring and Logging

### View Celery Tasks
Visit `http://localhost:5555` if you started Flower

### View Logs
```bash
tail -f backend/logs/app.log
```

### Redis Monitoring
```bash
redis-cli monitor
```

## Production Considerations

1. **Use a production WSGI server:**
   ```bash
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Configure proper CORS origins**
3. **Set up file size limits**
4. **Implement authentication/authorization**
5. **Add rate limiting**
6. **Set up proper logging and monitoring**
7. **Use environment-specific configuration**

## Troubleshooting

### Common Issues:

1. **Redis Connection Error:**
   - Check if Redis is running: `redis-cli ping`
   - Verify REDIS_URL in environment

2. **File Upload Errors:**
   - Check file size limits
   - Verify upload directory permissions

3. **Celery Tasks Not Starting:**
   - Check Celery worker logs
   - Verify Redis connection
   - Check task imports

4. **CORS Issues:**
   - Update allowed origins in main.py
   - Check frontend API URL configuration
