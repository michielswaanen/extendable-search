import { useState } from "react"

export type Scene = {
    id: string
    start: number
    end: number
}

export type Video = {
    id: string
    title: string
    fps: string
    duration: string
    scenes: number
    createdAt: string
}

const useVideos = () => {

    const [videos, setVideos] = useState<Video[]>([])

    const fetchVideos = async () => {
        const videos = await (await fetch('http://localhost:3001/videos')).json();

        for (const video of videos) {
            setVideos((prev) => [...prev, {
                id: video[0],
                title: video[1],
                fps: video[3],
                duration: video[4],
                scenes: video[6],
                createdAt: video[5]
            }])
        }
    }

    return {
        videos,
        fetchVideos
    }
}

export default useVideos