import { LucideChevronLeft } from "lucide-react"
import { useRouter } from "next/navigation"

type Props = {
    videoId: string
}

export default function DetailHeader(props: Props) {

    // /////////////////////////////////// //
    //                                     //
    //                 Hooks               //
    //                                     //
    // /////////////////////////////////// //

    const { push } = useRouter()

    // /////////////////////////////////// //
    //                                     //
    //                Actions              //
    //                                     //
    // /////////////////////////////////// //

    const handleBack = () => {
        push(`/feed`)
    }

    // /////////////////////////////////// //
    //                                     //
    //                 Render              //
    //                                     //
    // /////////////////////////////////// //

    return <div className="relative w-full">
        <div className="flex flex-row items-center gap-4">
            <button onClick={handleBack} className="p-2 bg-gray-50 rounded-lg border text-gray-500">
                <LucideChevronLeft size={24} />
            </button>
            <h1 className="text-3xl font-semibold">Video nr. {props.videoId}</h1>
        </div>
        <p className="text-gray-600">Our algorithm detected the following scenes inside the video</p>
    </div>
}