import { Clock1Icon, Tv2Icon } from "lucide-react"

export const SearchResults = () => {

    const renderVideo = (video: any) => {
        return <div className="flex flex-row items-center gap-2 hover:bg-gray-100 rounded-lg">
            <div className="h-12 border-gray-200 border w-12 rounded-lg bg-gray-100"></div>
            <div className="flex flex-col">
                <h2 className="text-lg font-medium">{video.title}</h2>
                <div className="flex flex-row gap-4">
                    <div className="flex flex-row gap-2 items-center">
                        <Clock1Icon size={16} className="relative text-slate-400" />
                        <p className="text-sm text-gray-500">2:30</p>
                    </div>
                    <div className="flex flex-row gap-2 items-center">
                        <Tv2Icon size={16} className="relative text-slate-400" />
                        <p className="text-sm text-gray-500">30 fps</p>
                    </div>
                </div>
            </div>
        </div>
    }

    return <div className="flex flex-col gap-4">
        {renderVideo({ title: "Video 1", description: "This is a video" })}
        {renderVideo({ title: "Video 2", description: "This is another video" })}
        {renderVideo({ title: "Video 3", description: "This is another video" })}
    </div>
}

