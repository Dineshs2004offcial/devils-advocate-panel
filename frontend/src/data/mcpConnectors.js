/**
 * MCP Connectors Specification and Mock/Static Metadata
 * Model Context Protocol endpoints, tools, resources, and live event data.
 */

export const MCP_CONNECTORS_MAP = {
  'active-protocol-mesh': {
    id: 'active-protocol-mesh',
    name: 'ActiveProtocolMesh',
    displayName: 'Active Protocol Mesh',
    route: '/mcp/active-protocol-mesh',
    iconName: 'Cpu',
    accentColor: '#818cf8',
    status: 'connected',
    category: 'Protocol Orchestration',
    shortDescription: 'Real-time multi-agent protocol bus & cross-agent synchronization mesh.',
    fullDescription: 'The Active Protocol Mesh coordinates stateful peer-to-peer MCP message channels between the Devil\'s Advocate Panel agents (Skeptical VC, Financial Analyst, Market Realist, and AI Lead Judge). It handles asynchronous tool arbitration, context routing, and LangGraph workflow checkpoints.',
    serverInfo: {
      protocolVersion: 'MCP 2024-11-05 (v1.0.0)',
      transport: 'STDIO / EventStream Bus',
      serverCommand: 'python -m app.mcp.mesh_server',
      endpoint: '127.0.0.1:8000/mcp/mesh',
      environment: 'Local Subprocess / Daemon',
      uptime: '99.99% (Active)',
      sdkVersion: '@modelcontextprotocol/sdk v1.0.4',
      memoryUsage: '38.4 MB',
      totalRequests: 1420,
      activeChannels: 4
    },
    connectionConfig: {
      latency: '4ms',
      timeout: '30,000ms',
      maxConcurrency: '32 pipelines',
      authMethod: 'Local IPC Pipe / JWT Session',
      retryPolicy: '3 attempts with jitter',
      keepAlive: 'Active ping every 10s',
      healthStatus: 'HEALTHY'
    },
    tools: [
      {
        name: 'broadcast_agent_challenge',
        description: 'Broadcasts an adversarial challenge payload across the agent mesh for peer review.',
        parameters: [
          { name: 'challenger_id', type: 'string', required: true, description: 'Source agent identifier (e.g. vc_agent)' },
          { name: 'target_id', type: 'string', required: true, description: 'Target agent (e.g. financial_analyst)' },
          { name: 'challenge_text', type: 'string', required: true, description: 'Substantive critique or risk question' }
        ],
        sampleOutput: '{"status": "delivered", "mesh_channel_id": "mesh_chan_8829", "latency_ms": 3.2}'
      },
      {
        name: 'sync_debate_state',
        description: 'Synchronizes current LangGraph checkpoint state across all connected MCP workers.',
        parameters: [
          { name: 'session_id', type: 'string', required: true, description: 'Active debate UUID' },
          { name: 'stage', type: 'string', required: true, description: 'Current pipeline stage (round1, rebuttal, judge)' }
        ],
        sampleOutput: '{"synced": true, "nodes_acknowledged": 4, "timestamp": 1726418800}'
      },
      {
        name: 'query_mesh_health',
        description: 'Inspects health and latency metrics for all registered sub-agents and tool servers.',
        parameters: [],
        sampleOutput: '{"healthy_nodes": 4, "degraded_nodes": 0, "avg_mesh_latency_ms": 3.8}'
      }
    ],
    resources: [
      { uri: 'mesh://channels/active', name: 'Active Agent Channels', mimeType: 'application/json' },
      { uri: 'mesh://logs/protocol', name: 'Protocol Audit Stream', mimeType: 'text/plain' }
    ],
    recentEvents: [
      { id: 'ev-1', time: 'Just now', type: 'HEARTBEAT', status: 'success', message: 'Mesh ping acknowledged by 4 agent daemons.' },
      { id: 'ev-2', time: '2m ago', type: 'STATE_SYNC', status: 'success', message: 'Debate checkpoint synchronised across LangGraph memory.' },
      { id: 'ev-3', time: '5m ago', type: 'TOOL_CALL', status: 'success', message: 'Broadcasted financial rebuttal to Skeptical VC.' },
      { id: 'ev-4', time: '12m ago', type: 'INIT', status: 'success', message: 'ActiveProtocolMesh established local IPC connection.' }
    ]
  },

  'web-research': {
    id: 'web-research',
    name: 'WebResearch MCP',
    displayName: 'Web Research MCP',
    route: '/mcp/web-research',
    iconName: 'Search',
    accentColor: '#38bdf8',
    status: 'connected',
    category: 'Intelligence Layer',
    shortDescription: 'Real-time market intelligence, competitor benchmarking & live web search.',
    fullDescription: 'The Web Research MCP connects the panel to real-time search APIs (DuckDuckGo, Tavily, Google Search) and HTML content scrapers (BeautifulSoup4) to extract market sizing (TAM/SAM), verify competitor claims, discover latest pricing models, and spot regulatory headwinds.',
    serverInfo: {
      protocolVersion: 'MCP 2024-11-05 (v1.0.0)',
      transport: 'STDIO / JSON-RPC 2.0',
      serverCommand: 'python -m app.mcp.web_server',
      endpoint: '127.0.0.1:8000/mcp/web',
      environment: 'Subprocess Pipe',
      uptime: '99.95% (Online)',
      sdkVersion: '@modelcontextprotocol/sdk v1.0.4',
      memoryUsage: '52.1 MB',
      totalRequests: 842,
      activeChannels: 2
    },
    connectionConfig: {
      latency: '14ms',
      timeout: '25,000ms',
      maxConcurrency: '8 concurrent queries',
      authMethod: 'Tavily / DDG API Keys',
      retryPolicy: '2 attempts with backoff',
      keepAlive: 'Every 30s',
      healthStatus: 'HEALTHY'
    },
    tools: [
      {
        name: 'search_web',
        description: 'Executes live web search queries and returns top ranked citations, snippets, and domain metadata.',
        parameters: [
          { name: 'query', type: 'string', required: true, description: 'Market research search query' },
          { name: 'max_results', type: 'number', required: false, description: 'Maximum number of results to fetch (default: 5)' }
        ],
        sampleOutput: '{"query": "AI Code Review Market Size 2025", "results_count": 5, "top_source": "Gartner Market Report"}'
      },
      {
        name: 'extract_competitor_intel',
        description: 'Scrapes domain landing pages and evaluates value propositions, pricing tiers, and customer traction.',
        parameters: [
          { name: 'domain', type: 'string', required: true, description: 'Competitor domain URL' },
          { name: 'aspects', type: 'array', required: false, description: 'Aspects to parse: ["pricing", "features", "customers"]' }
        ],
        sampleOutput: '{"domain": "competitor.ai", "pricing_model": "Usage-based $0.05/eval", "traction": "500+ teams"}'
      },
      {
        name: 'fetch_industry_multiples',
        description: 'Retrieves current EV/Revenue multiples, gross margin benchmarks, and median CAC for the given sector.',
        parameters: [
          { name: 'industry', type: 'string', required: true, description: 'Target sector (e.g. "B2B SaaS", "FinTech", "HealthTech")' }
        ],
        sampleOutput: '{"industry": "B2B SaaS", "median_ev_revenue": "6.8x", "gross_margin_avg": "78%"}'
      }
    ],
    resources: [
      { uri: 'web://cache/recent_searches', name: 'Search Query Cache', mimeType: 'application/json' },
      { uri: 'web://sources/verified', name: 'Verified Market Report Feeds', mimeType: 'text/markdown' }
    ],
    recentEvents: [
      { id: 'ev-w1', time: '1m ago', type: 'TOOL_CALL', status: 'success', message: 'Executed tool "search_web" for market growth rates.' },
      { id: 'ev-w2', time: '6m ago', type: 'SCRAPE', status: 'success', message: 'Extracted competitor pricing matrix via BeautifulSoup4 parser.' },
      { id: 'ev-w3', time: '18m ago', type: 'PING', status: 'success', message: 'DuckDuckGo / Tavily fallback endpoints verified healthy.' },
      { id: 'ev-w4', time: '35m ago', type: 'INIT', status: 'success', message: 'WebResearch MCP client initialized on port 8000.' }
    ]
  },

  'knowledge-base': {
    id: 'knowledge-base',
    name: 'Knowledge Base MCP',
    displayName: 'Knowledge Base MCP',
    route: '/mcp/knowledge-base',
    iconName: 'Network',
    accentColor: '#a855f7',
    status: 'connected',
    category: 'Knowledge RAG',
    shortDescription: 'Local RAG vector store powered by ChromaDB with startup benchmarks.',
    fullDescription: 'The Knowledge Base MCP provides dense semantic retrieval over historical pitch decks, VC investment memos, SaaS unit economics benchmarks, and regulatory compliance databases using ChromaDB and Sentence-Transformers embeddings.',
    serverInfo: {
      protocolVersion: 'MCP 2024-11-05 (v1.0.0)',
      transport: 'STDIO / Vector Socket',
      serverCommand: 'python -m app.mcp.kb_server',
      endpoint: 'chromadb://localhost:8000/collections/corpus',
      environment: 'Local ChromaDB Instance',
      uptime: '99.99% (Online)',
      sdkVersion: '@modelcontextprotocol/sdk v1.0.4',
      memoryUsage: '64.8 MB',
      totalRequests: 620,
      activeChannels: 1
    },
    connectionConfig: {
      latency: '6ms',
      timeout: '15,000ms',
      maxConcurrency: '16 vector searches',
      authMethod: 'Local File / Token',
      retryPolicy: '3 attempts',
      keepAlive: 'Persistent Memory Store',
      healthStatus: 'HEALTHY'
    },
    tools: [
      {
        name: 'query_vector_store',
        description: 'Performs semantic similarity search over indexed startup documents and VC case studies.',
        parameters: [
          { name: 'query_text', type: 'string', required: true, description: 'Natural language search query' },
          { name: 'k', type: 'number', required: false, description: 'Number of top matching chunks (default: 4)' },
          { name: 'filter_category', type: 'string', required: false, description: 'Metadata tag (e.g. "unit_economics", "tam_validation")' }
        ],
        sampleOutput: '{"retrieved_chunks": 4, "top_similarity_score": 0.892, "collection": "vc_benchmarks_2025"}'
      },
      {
        name: 'ingest_pitch_document',
        description: 'Chunks and embeds new pitch deck PDF or text document into the ChromaDB vector database.',
        parameters: [
          { name: 'document_text', type: 'string', required: true, description: 'Full text content or deck transcript' },
          { name: 'metadata', type: 'object', required: true, description: 'Dictionary with startup name, industry, and date' }
        ],
        sampleOutput: '{"chunks_created": 14, "embeddings_stored": 14, "status": "indexed"}'
      },
      {
        name: 'get_corpus_statistics',
        description: 'Returns total indexed document count, vector dimension, and embedding model specs.',
        parameters: [],
        sampleOutput: '{"total_documents": 240, "vector_dimension": 384, "model": "all-MiniLM-L6-v2"}'
      }
    ],
    resources: [
      { uri: 'kb://collections/vc_benchmarks', name: 'VC Benchmarks Corpus', mimeType: 'application/x-chroma' },
      { uri: 'kb://collections/legal_regulatory', name: 'Regulatory Standards', mimeType: 'application/x-chroma' }
    ],
    recentEvents: [
      { id: 'ev-k1', time: '3m ago', type: 'QUERY', status: 'success', message: 'Retrieved 4 benchmark chunks for SaaS retention curves.' },
      { id: 'ev-k2', time: '15m ago', type: 'EMBED', status: 'success', message: 'ChromaDB sentence-transformers vector index ping 0ms.' },
      { id: 'ev-k3', time: '1h ago', type: 'COLLECTION_SYNC', status: 'success', message: 'Corpus index verified (240 embedded chunks ready).' }
    ]
  },

  'postgresql': {
    id: 'postgresql',
    name: 'PostgreSQL MCP',
    displayName: 'PostgreSQL MCP',
    route: '/mcp/postgresql',
    iconName: 'Database',
    accentColor: '#10b981',
    status: 'connected',
    category: 'Storage & Audit',
    shortDescription: 'Persistent SQL storage for pitch evaluations, transcripts & audit logs.',
    fullDescription: 'The PostgreSQL MCP provides robust ACID relational storage for startup pitches, agent debate rounds, final scorecard evaluations, user feedback, and security audit logs using SQLAlchemy and pg8000/psycopg.',
    serverInfo: {
      protocolVersion: 'MCP 2024-11-05 (v1.0.0)',
      transport: 'Postgres Native / pg8000 Connector',
      serverCommand: 'python -m app.mcp.postgres_server',
      endpoint: 'postgresql://admin:***@127.0.0.1:5432/devils_advocate_panel',
      environment: 'Relational DB / Fallback SQLite',
      uptime: '99.99% (Healthy)',
      sdkVersion: '@modelcontextprotocol/sdk v1.0.4',
      memoryUsage: '48.3 MB',
      totalRequests: 1190,
      activeChannels: 4
    },
    connectionConfig: {
      latency: '2ms',
      timeout: '10,000ms',
      maxConcurrency: '20 connection pool size',
      authMethod: 'SCRAM-SHA-256 / SSL Mode',
      retryPolicy: 'Automatic pool reconnection',
      keepAlive: 'Connection pool heartbeat 15s',
      healthStatus: 'HEALTHY'
    },
    tools: [
      {
        name: 'save_pitch_evaluation',
        description: 'Persists complete multi-agent debate session, round-by-round arguments, and scorecard.',
        parameters: [
          { name: 'startup_name', type: 'string', required: true, description: 'Name of the startup' },
          { name: 'verdict', type: 'string', required: true, description: 'Final investment verdict' },
          { name: 'score', type: 'number', required: true, description: 'Composite panel score (0-100)' },
          { name: 'evaluation_payload', type: 'object', required: true, description: 'Full debate JSON tree' }
        ],
        sampleOutput: '{"evaluation_id": "eval_77192", "stored_at": "2026-09-15T21:40:00Z", "status": "committed"}'
      },
      {
        name: 'list_recent_evaluations',
        description: 'Queries recent pitch evaluation sessions with sorting and pagination.',
        parameters: [
          { name: 'limit', type: 'number', required: false, description: 'Max items to return (default: 20)' },
          { name: 'offset', type: 'number', required: false, description: 'Pagination offset' }
        ],
        sampleOutput: '{"total_count": 48, "returned_count": 20, "items": [{"id": "eval_1", "startup": "NexFlow AI"}]}'
      },
      {
        name: 'execute_sql_query',
        description: 'Executes sanitized read-only analytics query across historical evaluation aggregates.',
        parameters: [
          { name: 'query', type: 'string', required: true, description: 'SQL SELECT query string' }
        ],
        sampleOutput: '{"rows": 12, "columns": ["industry", "avg_score", "pass_rate"], "execution_time_ms": 1.4}'
      }
    ],
    resources: [
      { uri: 'postgres://tables/pitches', name: 'Startup Pitches Table', mimeType: 'application/sql' },
      { uri: 'postgres://tables/evaluations', name: 'Panel Evaluations & Scores', mimeType: 'application/sql' },
      { uri: 'postgres://tables/audit_logs', name: 'Debate Audit Logs', mimeType: 'application/sql' }
    ],
    recentEvents: [
      { id: 'ev-p1', time: '1m ago', type: 'TRANSACTION', status: 'success', message: 'Committed evaluation session #eval_77192 successfully.' },
      { id: 'ev-p2', time: '8m ago', type: 'POOL_CHECK', status: 'success', message: 'Connection pool active (4 connected, 16 idle).' },
      { id: 'ev-p3', time: '30m ago', type: 'SCHEMA_MIGRATE', status: 'success', message: 'SQLAlchemy Base metadata tables verified.' }
    ]
  },

  'report-pdf': {
    id: 'report-pdf',
    name: 'Report & PDF MCP',
    displayName: 'Report & PDF MCP',
    route: '/mcp/report-pdf',
    iconName: 'FileText',
    accentColor: '#f59e0b',
    status: 'connected',
    category: 'Document Synthesis',
    shortDescription: 'Executive summary & PDF dossier compiler for venture capitalists.',
    fullDescription: 'The Report & PDF MCP compiles adversarial multi-agent debate transcripts, financial audit matrices, market competitor benchmarks, and final AI Judge verdicts into printable, executive-ready PDF, HTML, and Markdown dossiers.',
    serverInfo: {
      protocolVersion: 'MCP 2024-11-05 (v1.0.0)',
      transport: 'STDIO / PDF Renderer',
      serverCommand: 'python -m app.mcp.report_server',
      endpoint: '127.0.0.1:8000/mcp/report',
      environment: 'Subprocess PDF Engine',
      uptime: '99.98% (Online)',
      sdkVersion: '@modelcontextprotocol/sdk v1.0.4',
      memoryUsage: '44.7 MB',
      totalRequests: 430,
      activeChannels: 1
    },
    connectionConfig: {
      latency: '18ms',
      timeout: '40,000ms',
      maxConcurrency: '4 render workers',
      authMethod: 'Internal IPC / Token',
      retryPolicy: '2 attempts with queue buffer',
      keepAlive: 'Daemon Worker Active',
      healthStatus: 'HEALTHY'
    },
    tools: [
      {
        name: 'compile_executive_dossier',
        description: 'Synthesizes complete evaluation JSON into formatted PDF document with charts & scorecard.',
        parameters: [
          { name: 'evaluation_id', type: 'string', required: true, description: 'Evaluation UUID' },
          { name: 'format', type: 'string', required: false, description: 'Output format: "pdf" | "html" | "markdown"' },
          { name: 'include_transcripts', type: 'boolean', required: false, description: 'Include verbatim agent round 1 & 2 dialogue' }
        ],
        sampleOutput: '{"file_name": "NexFlow_AI_VC_Dossier.pdf", "file_size_kb": 284, "download_url": "/api/reports/dl/1"}'
      },
      {
        name: 'export_markdown_summary',
        description: 'Generates clean GitHub-flavored markdown summary of the investment committee consensus.',
        parameters: [
          { name: 'evaluation_id', type: 'string', required: true, description: 'Evaluation UUID' }
        ],
        sampleOutput: '{"status": "compiled", "lines": 142, "format": "markdown"}'
      }
    ],
    resources: [
      { uri: 'report://templates/executive_dossier', name: 'Executive PDF Template', mimeType: 'text/html' },
      { uri: 'report://exports/archive', name: 'Generated Report Archive', mimeType: 'application/pdf' }
    ],
    recentEvents: [
      { id: 'ev-r1', time: '4m ago', type: 'EXPORT', status: 'success', message: 'Compiled executive PDF dossier (284 KB).' },
      { id: 'ev-r2', time: '22m ago', type: 'TEMPLATE_LOAD', status: 'success', message: 'Loaded modern VC committee dossier theme.' },
      { id: 'ev-r3', time: '45m ago', type: 'INIT', status: 'success', message: 'PDF generator subprocess ready.' }
    ]
  }
};

export const MCP_CONNECTORS_LIST = Object.values(MCP_CONNECTORS_MAP);

export function getMcpConnectorById(id) {
  if (!id) return null;
  const normalizedId = String(id).toLowerCase().trim();
  return (
    MCP_CONNECTORS_MAP[normalizedId] ||
    MCP_CONNECTORS_LIST.find(
      (c) =>
        c.id.toLowerCase() === normalizedId ||
        c.name.toLowerCase().replace(/[^a-z0-9]/g, '-') === normalizedId ||
        c.route.endsWith(normalizedId)
    ) ||
    null
  );
}
