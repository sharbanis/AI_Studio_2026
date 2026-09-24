import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

const FLOW_ID = '069c4b88-7853-416d-87f9-d6f7df88acfe'
// Set VITE_LANGFLOW_API_KEY in your environment (or a local .env file).
const API_KEY = import.meta.env.VITE_LANGFLOW_API_KEY
const BASE_URL = 'http://localhost:7860'

export default function App() {
  const [issueKey, setIssueKey] = useState('KAN-1')
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function runFlow() {
    const key = issueKey.trim()
    if (!key || loading) return
    setLoading(true)
    setError('')
    setOutput('')
    try {
      const res = await fetch(`${BASE_URL}/api/v1/run/${FLOW_ID}?stream=false`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': API_KEY,
        },
        body: JSON.stringify({
          output_type: 'chat',
          input_type: 'text',
          input_value: key,
          session_id: `ui-${Date.now()}`,
        }),
      })
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${await res.text()}`)
      }
      const data = await res.json()
      const text = data?.outputs?.[0]?.outputs?.[0]?.results?.message?.text
      if (text) setOutput(text)
      else setError('No output text found in the response.')
    } catch (e) {
      setError(e?.message || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>Bug Triage Chatbot</h1>
        <p>Langflow · Bug Triage v0.3</p>
      </header>

      <div className="input-row">
        <input
          type="text"
          value={issueKey}
          onChange={(e) => setIssueKey(e.target.value)}
          placeholder="Enter Jira issue key (e.g. KAN-1)"
          onKeyDown={(e) => e.key === 'Enter' && runFlow()}
        />
        <button onClick={runFlow} disabled={loading}>
          {loading ? 'Running…' : 'Run'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {output ? (
        <div className="output">
          <ReactMarkdown>{output}</ReactMarkdown>
        </div>
      ) : (
        !loading && (
          <div className="empty">
            Enter an issue key and press <strong>Run</strong> to generate a triage report.
          </div>
        )
      )}
    </div>
  )
}
