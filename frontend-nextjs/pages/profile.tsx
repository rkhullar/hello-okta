import Head from 'next/head'
import { useSession } from 'next-auth/react'
import Layout from '$components/layout'

export default function Profile() {
  // const [session, loading] = useSession()
  const { data: session } = useSession()
  return (
    <Layout>
      <Head>
        <title>Profile</title>
      </Head>
      <section>
        <p>profile</p>
        {session && session.accessToken}
      </section>
    </Layout>
  )
}