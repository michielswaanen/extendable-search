import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Container from '@/components/global/Container'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Masterproef',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main className="flex w-full bg-white h-screen justify-center align">

          <Container>
            {children}
          </Container>
        </main>
      </body>
    </html>
  )
}
