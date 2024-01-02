"use client"

import Header from "@/components/global/Header";
import SearchBox from "@/components/search/SearchBox";
import { SearchResults } from "@/components/search/SearchResults";
import { useMount } from "@/core/useMount";
import useVideos from "@/core/useVideos";
import { useRouter } from 'next/navigation'

export default function Feed() {

  // /////////////////////////////////// //
  //                                     //
  //                 Hooks               //
  //                                     //
  // /////////////////////////////////// //

  const { fetchVideos, videos } = useVideos()
  const { push } = useRouter()

  useMount(() => {
    fetchVideos();
  })

  // /////////////////////////////////// //
  //                                     //
  //                Actions              //
  //                                     //
  // /////////////////////////////////// //

  const handleRedirect = (videoId: string) => {
    push(`/video/${videoId}`)
  }

  // /////////////////////////////////// //
  //                                     //
  //                Rendering            //
  //                                     //
  // /////////////////////////////////// //

  return (
    <>
      <Header />
      <div className="h-12" />
      <SearchBox />
      <div className="h-12" />
      <SearchResults videos={videos} onResultClick={handleRedirect} />
    </>
  )
}
