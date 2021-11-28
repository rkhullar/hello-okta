import Head from 'next/head'
import Link from 'next/link'

// {children: React.ReactNode, home?: boolean}
export default function Layout({ children, home }) {
  return (
    <>
      <Head>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>{children}</main>
      {!home && (
        <Link href="/">
          <a>← Back to home</a>
        </Link>
      )}
    </>
  )
}