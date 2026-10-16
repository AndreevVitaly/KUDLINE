type LogoProps = {
  variant?: 'horizontal' | 'mark'
  theme?: 'light' | 'dark'
  className?: string
}

import {Link} from 'react-router-dom'

export function Logo({variant = 'horizontal', theme = 'light', className = ''}: LogoProps) {
  const suffix = theme === 'light' ? 'light' : 'dark'
  const markSrc = `/brand/kudline-mark-${suffix}.webp`
  const horizontalSrc = `/brand/kudline-logo-horizontal-${suffix}.webp`

  return (
    <Link className={`brand-logo brand-logo--${variant} ${className}`.trim()} to="/" aria-label="ООО «КУДЛАЙН»">
      {variant === 'mark' ? (
        <img src={markSrc} alt="ООО «КУДЛАЙН»" />
      ) : (
        <img className="brand-logo__horizontal" src={horizontalSrc} alt="ООО «КУДЛАЙН»" />
      )}
    </Link>
  )
}
