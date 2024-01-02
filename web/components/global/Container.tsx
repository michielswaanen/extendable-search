export default function Container({ children }: any) {
    return <div className="flex flex-col h-full w-1/2 bg-gray-50 p-16 border-x border-gray-100">
        { children }
    </div>
}