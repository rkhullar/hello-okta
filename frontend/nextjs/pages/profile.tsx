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
        <p>profile</p>
        {session && JSON.stringify(session.user)}
        <p>id_token</p>
        {session && session.id_token}
        <p>access_token</p>
        {session && session.access_token}
      </section>
    </Layout>
  )
}