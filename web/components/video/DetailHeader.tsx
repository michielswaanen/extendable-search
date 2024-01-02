type Props = {
    videoId: string
}

export default function DetailHeader(props: Props) {
    return <div className="relative w-full">
        <h1 className="text-3xl font-semibold">Video nr. {props.videoId}</h1>
        <p className="text-gray-600">Our algorithm detected the following scenes inside the video</p>
  </div>
}