import Head from 'next/head'
import { useSession } from 'next-auth/react'
import Layout from '$components/layout'

async function hello(session) {
  const base_url = 'http://0.0.0.0:8000'
  const response = await fetch(`${base_url}/profile`, {
    headers: {
      'Authorization': `Bearer ${session.access_token}`
    }
  })
  const data = response.json()
  console.log(data)
}

export default function Backend() {
  const { data: session } = useSession()
  return (
    <Layout>
      <Head>
        <title>Backend</title>
      </Head>
      <section>
        <button onClick={() => hello(session)}>profile</button>
      </section>
    </Layout>
  )
}