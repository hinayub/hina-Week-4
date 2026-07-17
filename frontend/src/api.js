// Client for the Django research API.

async function parseError(res) {
  let message = `Request failed (${res.status})`
  try {
    const data = await res.json()
    if (data?.error) message = data.error
  } catch {
    // response wasn't JSON; keep the default message
  }
  throw new Error(message)
}

/** Ask the agent a question. Returns the stored result with answer + sources. */
export async function research(query) {
  const res = await fetch('/api/research/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  })
  if (!res.ok) return parseError(res)
  return res.json()
}

/** Fetch past research queries, newest first. */
export async function getHistory() {
  const res = await fetch('/api/research/history/')
  if (!res.ok) return parseError(res)
  const data = await res.json()
  return Array.isArray(data) ? data : (data.results ?? [])
}
