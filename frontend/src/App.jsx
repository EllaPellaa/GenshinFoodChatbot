import { useState } from 'react'
import './App.css'

// Generate a stable session ID per browser tab
const SESSION_ID = `session-${Math.random().toString(36).slice(2, 9)}`

// API address
const API_BASE = 'http://localhost:8000'

function App() {
  const [messages, setMessages] = useState([])
  const [isStreaming, setIsStreaming] = useState(false)
  const [steamingEnabled, setStreamingEnabled] = useState(true)
  const [lastUsage, setLastUsage] = useState(null)
  const [error, setError] = useState(null)

  async function sendMessages(text) {
    if (!text.trim() || isStreaming) return

    setError(null)
    const userMsg = { role: 'user', content: text }
    const updatedMessages = [...messages, userMsg]
    setMessages(updatedMessages)
    setIsStreaming(true)

    // Pass history as-is - the backend converts it to the right format
    // History is everything before the new use message.
    const history = messages

    try {
      if (streamingEnabled) {
        await streamResponse(text, history, updatedMessages)
      } else {
        await fetchResponse(text, history, updatedMessaes)
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setIsStreaming(false)
    }
  }

  // ----- Fetch data with streaming enabled -----
  async function streamResponse(message, history, currentMessages) {
    const response = await fetch(`${API_BASE}/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history, session_id: SESSION_ID}),
    })

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail || `Server error: ${response.status}`)
    }

    // Add an empty assistant message slot - filled in as chunks arrive
    const assistantIndex = currentMessages.length
    setMessages([...currentMessages, { role: 'assistant', content: ''}])

    // GetReader() method of ReadableStream interface creates a reader and locks the stream to it
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    let fullText = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      
      // SSE events are separated by "\n\n"
      const events = buffer.split('\n\n')
      buffer = events.pop() // last item may be incomplete

      for (const event of events) {
        if (!event.startsWith('data: ')) continue
        const data = JSON.parse(event.slice(6))

        if (data.type === 'text') {
          fullText += data.content

          setMessages((prev) => {
            const updated = [...prev]
            updated[assistantIndex] = { role: 'assistant', content: fullText }
            return updated
          })
        } else if (data.type === 'done') {
          // We don't need the usage for this one, would be updated here if it was used.
        }
      }
    }
  }

  // ----- Regular fetch with no streaming -----
  async function fetchResponse(message, history, currentMessage) {
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, history, session_id: SESSION_ID }),
    })

    if (!response.ok) {
      const err = await response.json()
      throw new Error(err.detail || `Server error: ${response.status}`)
    }

    const data = await response.json()
    setMessages([...currentMessage, { role: 'assistant', content: data.response}])
    // Updating usage would be here if we needed it
  }

  function clearChat() {
    setMessages([])
    setLastUsage(null)
    setError(null)
  }

  return (
    <div className='app'>
      <section id="center">
        <div>
          <h1>Genshin Impact Recipe Chatbot</h1>
        </div>
        
      </section>

      <section id="next-steps">
        
      </section>

      <section id="spacer"></section>
    </div>
  )
}

export default App
