import Head from 'next/head'
import Link from 'next/link'
import Layout from '../components/layout'

export default function Home() {
  return (
    <Layout>
      <Head>
        <title>Hello Okta</title>
      </Head>
      <section>
        <p>hello world</p>
      </section>
    </Layout>
  )
}
