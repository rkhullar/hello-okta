import Head from 'next/head'
import Link from 'next/link'
import { useSession, signIn, signOut } from 'next-auth/react'

interface Props {
  children: React.ReactNode
  home?: boolean
}

const Layout: React.FunctionComponent<Props> = ({ children, home }) => {
  // const [session, loading] = useSession()
  const { data: session } = useSession()
  let button
  if (session)
    button = <button onClick={() => signOut()}>Logout</button>
  else
    button = <button onClick={() => signIn()}>Login</button>
  return (
    <>
      <Head>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <section>
        {!home && (
          <Link href="/">
            <a>Home</a>
          </Link>
        )}
        {button}
      </section>
      <hr/>
      <main>{children}</main>
      <hr/>
      <footer>
      </footer>
    </>
  )
}

export default Layout