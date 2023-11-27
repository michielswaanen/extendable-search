"use client"

import Container from "@/components/Container";
import Header from "@/components/Header";
import SearchBox from "@/components/SearchBox";
import { SearchResults } from "@/components/SearchResults";
import useVideos from "@/core/useVideos";
import { useEffect } from "react";

export default function Home() {

  const { fetchVideos, videos } = useVideos()

  useEffect(() => {
    console.log("fetching videos")
    fetchVideos();
  }, [])

  return (
    <main className="flex w-full bg-white h-screen justify-center align">

      <Container>
        <Header />
        <div className="h-12" />
        <SearchBox />
        <div className="h-12" />
        <SearchResults videos={videos} />
      </Container>


    </main>
  )
}
