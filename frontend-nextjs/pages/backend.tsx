import Head from 'next/head'
import Layout from '$components/layout'
import { useSession } from 'next-auth/react'
import { useState } from 'react'

async function loadProfile(base_url: string, session, callback) {
  const response = await fetch(`${base_url}/profile`, {
    headers: {
      'Authorization': `Bearer ${session.access_token}`
    }
  })
  const data = await response.json()
  callback(data)
}

async function loadHello(base_url: string, callback) {
  const response = await fetch(`${base_url}/hello`)
  const data = await response.json()
  callback(data)
}

export async function getServerSideProps() {
  return {props: {
    fastapi_url:  process.env.FASTAPI_URL
  }}
}

export default function Backend({ fastapi_url }) {
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
        <button onClick={() => loadProfile(fastapi_url, session, setResult)}>profile</button>
        <button onClick={() => loadHello(fastapi_url, setResult)}>hello</button>
        <button onClick={() => setResult(null)}>clear</button>
        {result && (
          <p>{JSON.stringify(result)}</p>
        )}
      </section>
    </Layout>
  )
}