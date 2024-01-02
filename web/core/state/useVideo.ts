import { useState } from "react"
import { Video } from "./useVideos";

const useVideo = () => {

    const [video, setVideo] = useState<Video | undefined>()

    const fetchVideo = async (videoId: string) => {
        const url = `http://localhost:3001/videos/${videoId}`
        const videos = await (await fetch(url)).json();

        for (const video of videos) {
            setVideo({
                id: video[0],
                title: video[1],
                fps: video[3],
                duration: video[4],
                scenes: video[6],
                createdAt: video[5]
            })
        }
    }

    return {
        video,
        fetchVideo
    }
}

export default useVideo