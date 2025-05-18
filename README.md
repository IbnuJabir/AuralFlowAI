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