import Head from 'next/head'
import { useSession } from 'next-auth/client'
import Layout from '../components/layout'

export default function Profile() {
  const [session, loading] = useSession()
  console.log(session)
  return (
    <Layout>
      <Head>
        <title>Profile</title>
      </Head>
      <section>
        <p>profile</p>
      </section>
    </Layout>
  )
}