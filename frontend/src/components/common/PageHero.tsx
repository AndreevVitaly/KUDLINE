import {Breadcrumbs} from './Breadcrumbs'

export function PageHero({title, subtitle, crumbs}:{title:string; subtitle:string; crumbs?:{label:string;to?:string}[]}) {
  return <section className="page-hero"><div className="shell">{crumbs&&<Breadcrumbs items={crumbs}/>}<span className="eyebrow">ООО «КУДЛАЙН»</span><h1>{title}</h1><p>{subtitle}</p></div></section>
}
