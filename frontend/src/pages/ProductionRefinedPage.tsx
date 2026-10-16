import {Link} from 'react-router-dom'
import {Factory, MapPin} from 'lucide-react'
import {PageHero} from '../components/common/PageHero'
import {Seo} from '../components/common/Seo'

const cycle = ['Проектирование', 'Производство', 'Контроль', 'Доставка', 'Монтаж', 'Готовый объект']

export function ProductionRefinedPage() {
  return <>
    <Seo title="Производство металлоконструкций — КУДЛАЙН" description="Собственное производство металлоконструкций ООО «КУДЛАЙН» в Выборге."/>
    <PageHero title="Производство" subtitle="Собственная производственная площадка в Выборге" crumbs={[{label: 'Производство'}]}/>
    <section className="section production-page"><div className="shell content-grid">
      <div><Factory className="page-icon"/><h2>Площадка в Выборге</h2></div>
      <div className="rich-copy"><p>Производственная площадка объединяет изготовление конструкций и контроль в едином рабочем процессе.</p><div className="address"><MapPin/><strong>г. Выборг,<br/>ул. Промышленная, д. 19</strong></div></div>
    </div></section>
    <section className="section"><div className="shell">
      <span className="section-no">Производственный цикл</span>
      <div className="cycle-line">{cycle.map((item, index) => <div className="cycle-item" key={item}><span>{String(index + 1).padStart(2, '0')}</span><strong>{item}</strong></div>)}</div>
      <div className="section-cta"><Link className="button" to="/request">Отправить проект на расчёт</Link></div>
    </div></section>
  </>
}
