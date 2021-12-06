import Head from 'next/head'
import { useSession } from 'next-auth/react'
import Layout from '$components/layout'

export default function Profile() {
  const { data: session } = useSession()
  return (
    <Layout>
      <Head>
        <title>Profile</title>
      </Head>
      <section>
        <p>session</p>
        {JSON.stringify(session)}
      </section>
    </Layout>
  )
}