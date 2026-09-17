flowchart TD

subgraph group_frontend["Frontend SPA"]
  node_frontend_bootstrap["Vite bootstrap<br/>SPA entry<br/>[main.jsx]"]
  node_app["App composition<br/>UI root<br/>[App.jsx]"]
  node_theme_input["Theme input<br/>creation UI<br/>[ThemeInput.jsx]"]
  node_story_generator_ui["Story generator<br/>generation UI<br/>[StoryGenerator.jsx]"]
  node_loading_status["Loading status<br/>job status UI<br/>[LoadingStatus.jsx]"]
  node_story_views["Story loader &amp; game<br/>story UI"]
end

subgraph group_api["Backend API"]
  node_backend_app["Backend application<br/>Python entry<br/>[main.py]"]
  node_story_api["Story API<br/>router<br/>[story.py]"]
  node_job_api["Job API<br/>router<br/>[job.py]"]
  node_api_contracts["API contracts<br/>request/response schemas"]
end

subgraph group_core["Generation Core"]
  node_story_generator{{"Generation orchestrator<br/>core service<br/>[story_generator.py]"}}
  node_prompts["Prompt templates<br/>generation prompts<br/>[prompts.py]"]
  node_core_models["Core domain models<br/>domain representations<br/>[models.py]"]
  node_config["Configuration<br/>environment settings<br/>[config.py]"]
end

subgraph group_data["Persistence"]
  node_database[("Database session<br/>SQLite access<br/>[database.py]")]
  node_job_record[("Job records<br/>persistence model<br/>[job.py]")]
  node_story_record[("Story records<br/>persistence model<br/>[story.py]")]
  node_sqlite[("SQLite storage<br/>local database<br/>[database.db]")]
end

node_frontend_bootstrap -->|"mounts"| node_app
node_app -->|"composes"| node_theme_input
node_app -->|"composes"| node_story_generator_ui
node_app -->|"composes"| node_loading_status
node_app -->|"composes"| node_story_views
node_theme_input -->|"theme"| node_story_generator_ui
node_story_generator_ui -->|"starts generation"| node_job_api
node_loading_status -->|"reads status"| node_job_api
node_story_views -->|"loads stories"| node_story_api
node_backend_app -->|"registers"| node_story_api
node_backend_app -->|"registers"| node_job_api
node_story_api -->|"uses"| node_api_contracts
node_job_api -->|"uses"| node_api_contracts
node_job_api -->|"orchestrates"| node_story_generator
node_story_api -->|"reads"| node_story_record
node_story_generator -->|"builds prompts"| node_prompts
node_story_generator -->|"uses provider settings"| node_config
node_story_generator -->|"creates"| node_core_models
node_story_generator -->|"updates lifecycle"| node_job_record
node_story_generator -->|"persists result"| node_story_record
node_job_record -->|"uses session"| node_database
node_story_record -->|"uses session"| node_database
node_database -->|"stores"| node_sqlite

click node_frontend_bootstrap "https://github.com/dfwjani21/full-stack-genai-/blob/main/frontend/src/main.jsx"
click node_app "https://github.com/dfwjani21/full-stack-genai-/blob/main/frontend/src/App.jsx"
click node_theme_input "https://github.com/dfwjani21/full-stack-genai-/blob/main/frontend/src/components/ThemeInput.jsx"
click node_story_generator_ui "https://github.com/dfwjani21/full-stack-genai-/blob/main/frontend/src/components/StoryGenerator.jsx"
click node_loading_status "https://github.com/dfwjani21/full-stack-genai-/blob/main/frontend/src/components/LoadingStatus.jsx"
click node_backend_app "https://github.com/dfwjani21/full-stack-genai-/blob/main/backend/main.py"
click node_story_api "https://github.com/dfwjani21/full-stack-genai-/blob/main/backend/routers/story.py"
click node_job_api "https://github.com/dfwjani21/full-stack-genai-/blob/main/backend/routers/job.py"
click node_story_generator "https://github.com/dfwjani21/full-stack-genai-/blob/main/backend/core/story_generator.py"
click node_prompts "https://github.com/dfwjani21/full-stack-genai-/blob/main/backend/core/prompts.py"
click node_core_models "https://github.com/dfwjani21/full-stack-genai-/blob/main/backend/core/models.py"
click node_config "https://github.com/dfwjani21/full-stack-genai-/blob/main/backend/core/config.py"
click node_database "https://github.com/dfwjani21/full-stack-genai-/blob/main/backend/db/database.py"
click node_job_record "https://github.com/dfwjani21/full-stack-genai-/blob/main/backend/models/job.py"
click node_story_record "https://github.com/dfwjani21/full-stack-genai-/blob/main/backend/models/story.py"
click node_sqlite "https://github.com/dfwjani21/full-stack-genai-/blob/main/backend/database.db"

classDef toneNeutral fill:#f8fafc,stroke:#334155,stroke-width:1.5px,color:#0f172a
classDef toneBlue fill:#dbeafe,stroke:#2563eb,stroke-width:1.5px,color:#172554
classDef toneAmber fill:#fef3c7,stroke:#d97706,stroke-width:1.5px,color:#78350f
classDef toneMint fill:#dcfce7,stroke:#16a34a,stroke-width:1.5px,color:#14532d
classDef toneRose fill:#ffe4e6,stroke:#e11d48,stroke-width:1.5px,color:#881337
classDef toneIndigo fill:#e0e7ff,stroke:#4f46e5,stroke-width:1.5px,color:#312e81
classDef toneTeal fill:#ccfbf1,stroke:#0f766e,stroke-width:1.5px,color:#134e4a
class node_frontend_bootstrap,node_app,node_theme_input,node_story_generator_ui,node_loading_status,node_story_views toneBlue
class node_backend_app,node_story_api,node_job_api,node_api_contracts toneAmber
class node_story_generator,node_prompts,node_core_models,node_config toneMint
class node_database,node_job_record,node_story_record,node_sqlite toneRose
