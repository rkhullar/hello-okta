import Head from 'next/head'
import Link from 'next/link'

interface Props {
  children: React.ReactNode
  home?: boolean
}

const Layout: React.FunctionComponent<Props> = ({ children, home }) => (
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

export default Layout