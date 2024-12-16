import { Extension } from '@tiptap/core'
import { Plugin } from '@tiptap/pm/state'
import { EditorView } from '@tiptap/pm/view'

export interface ImageResizeOptions {
    minWidth?: number
    maxWidth?: number
}

declare module '@tiptap/core' {
    interface Commands<ReturnType> {
        imageResize: {
            setImageWidth: (width: number) => ReturnType
        }
    }
}

export const ImageResize = Extension.create<ImageResizeOptions>({
    name: 'imageResize',

    addOptions() {
        return {
            minWidth: 100,
            maxWidth: 1000,
        }
    },

    addProseMirrorPlugins() {
        let dragging = false
        let startX = 0
        let startWidth = 0
        let $img: HTMLImageElement | null = null

        const createResizeHandle = (img: HTMLImageElement) => {
            const wrapper = document.createElement('div')
            wrapper.className = 'image-wrapper'
            img.parentNode?.insertBefore(wrapper, img)
            wrapper.appendChild(img)

            const handle = document.createElement('div')
            handle.className = 'resize-handle'
            wrapper.appendChild(handle)

            return handle
        }

        return [
            new Plugin({
                props: {
                    handleDOMEvents: {
                        mousedown: (view: EditorView, event: MouseEvent) => {
                            const target = event.target as HTMLElement

                            if (!target.classList.contains('resize-handle')) {
                                return false
                            }

                            dragging = true
                            startX = event.pageX
                            $img = target.parentElement?.querySelector('img') || null
                            startWidth = $img?.offsetWidth || 0

                            target.parentElement?.classList.add('resize-active')

                            return true
                        },
                        mousemove: (_view: EditorView, event: MouseEvent) => {
                            if (!dragging || !$img) return false

                            const currentX = event.pageX
                            const diffX = currentX - startX
                            const newWidth = Math.max(
                                this.options.minWidth || 100,
                                Math.min(startWidth + diffX, this.options.maxWidth || 1000)
                            )

                            $img.style.width = `${newWidth}px`
                            return true
                        },
                        mouseup: (_view: EditorView, _event: MouseEvent) => {
                            if (!dragging) return false

                            dragging = false
                            $img?.parentElement?.classList.remove('resize-active')
                            $img = null

                            return true
                        },
                    },
                },
            }),
        ]
    },

    onCreate() {
        // Agregar manejadores de resize a las imágenes existentes
        const images = document.querySelectorAll('.ProseMirror img') as NodeListOf<HTMLImageElement>
        images.forEach((img) => {
            if (!img.parentElement?.classList.contains('image-wrapper')) {
                const wrapper = document.createElement('div')
                wrapper.className = 'image-wrapper'
                img.parentNode?.insertBefore(wrapper, img)
                wrapper.appendChild(img)

                const handle = document.createElement('div')
                handle.className = 'resize-handle'
                wrapper.appendChild(handle)
            }
        })
    },
})