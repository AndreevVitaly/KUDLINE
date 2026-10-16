import {Component, type ErrorInfo, type ReactNode} from 'react'

type Props = {children: ReactNode}
type State = {error: Error | null}

export class AppErrorBoundary extends Component<Props, State> {
  state: State = {error: null}

  static getDerivedStateFromError(error: Error): State {
    return {error}
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('KUDLINE frontend error', error, info)
  }

  render() {
    if (this.state.error) {
      return (
        <main className="page-state shell" role="alert">
          <h1>Не удалось загрузить страницу</h1>
          <p>Обновите страницу. Если ошибка повторится, сообщите разработчику.</p>
          <button className="button" type="button" onClick={() => window.location.reload()}>
            Обновить
          </button>
        </main>
      )
    }

    return this.props.children
  }
}
