import {useState} from 'react'
import Head from 'next/head'
import { useSession } from 'next-auth/react'
import Layout from '$components/layout'

async function hello(session, callback) {
  const base_url = 'http://0.0.0.0:8000'
  const response = await fetch(`${base_url}/profile`, {
    headers: {
      'Authorization': `Bearer ${session.access_token}`
    }
  })
  const data = await response.json()
  callback(data)
}

export default function Backend() {
  const { data: session } = useSession()
  const [data, setData] = useState(null)
  return (
    <Layout>
      <Head>
        <title>Backend</title>
      </Head>
      <section>
        <button onClick={() => hello(session, setData)}>profile</button>
        <p>{JSON.stringify(data)}</p>
      </section>
    </Layout>
  )
}