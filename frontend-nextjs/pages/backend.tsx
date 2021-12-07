import Head from 'next/head'
import { useSession } from 'next-auth/react'
import Layout from '$components/layout'

export default function Backend() {
  const { data: session } = useSession()
  return (
    <Layout>
      <Head>
        <title>Backend</title>
      </Head>
      <section>
        <p>tbd</p>
      </section>
    </Layout>
  )
}