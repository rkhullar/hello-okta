import Head from 'next/head'
import Layout from '$components/layout'
import { useSession } from 'next-auth/react'
import { useState } from 'react'

async function loadProfile(session, callback) {
  const base_url = 'http://0.0.0.0:8000'
  const response = await fetch(`${base_url}/profile`, {
    headers: {
      'Authorization': `Bearer ${session.access_token}`
    }
  })
  const data = await response.json()
  callback(data)
}

async function loadHello(callback) {
  const base_url = 'http://0.0.0.0:8000'
  const response = await fetch(`${base_url}/hello`)
  const data = await response.json()
  callback(data)
}

export default function Backend() {
  const { data: session } = useSession()
  const [count, setCount] = useState(0)
  const [result, setResult] = useState(null)
  return (
    <Layout>
      <Head>
        <title>Backend</title>
      </Head>
      <section>
        <button onClick={() => setCount(count + 1)}>count={count}</button>
        <button onClick={() => loadProfile(session, setResult)}>profile</button>
        <button onClick={() => loadHello(setResult)}>hello</button>
        <button onClick={() => setResult(null)}>clear</button>
        {result && (
          <p>{JSON.stringify(result)}</p>
        )}
      </section>
    </Layout>
  )
}