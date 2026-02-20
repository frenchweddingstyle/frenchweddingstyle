import React from 'react';
import { Venue } from '../types';

interface VenueCardProps {
  venue: Venue;
  index: number;
}

const VenueCard: React.FC<VenueCardProps> = ({ venue, index }) => {
  const shortName = venue.ctaName || venue.name;

  return (
    <div className="flex flex-col space-y-6 group/card" id={venue.id}>
      {/* 1. Header: Name & Region */}
      <div className="text-center md:text-left">
        <h2 className="text-3xl md:text-4xl lg:text-5xl text-fws-dark mb-1 leading-tight">
          {venue.name}
        </h2>
        <p className="text-fws-green text-[10px] tracking-[0.4em] font-bold uppercase font-sans">
          {venue.location}
        </p>
      </div>

      {/* 2. Venue Description */}
      <div className="max-w-4xl">
        <p className="text-fws-grey text-sm font-light leading-relaxed">
          {venue.description}
        </p>
      </div>

      {/* 3. Venue Image */}
      <div className="w-full overflow-hidden shadow-lg rounded-sm">
        <div className="aspect-[16/9] overflow-hidden bg-fws-light relative">
          <img 
            src={venue.imageUrl} 
            alt={venue.name} 
            className="w-full h-full object-cover transition-transform duration-[5s] group-hover/card:scale-105"
            loading="lazy"
          />
          <span className="absolute bottom-2 right-2 text-[8px] uppercase tracking-widest text-white/40 pointer-events-none select-none">
            Photo credit
          </span>
        </div>
      </div>

      {/* 4. Vertical Venue Table */}
      <div className="max-w-xl">
        <div className="border border-fws-green/20 rounded-lg overflow-hidden bg-white shadow-sm">
          <table className="w-full text-left border-collapse">
            <tbody className="divide-y divide-fws-green/10">
              <tr className="hover:bg-fws-light/30 transition-colors">
                {/* Reduced padding in column 1 (th) using px-1 */}
                <th className="w-[100px] py-2 px-2 bg-fws-light text-[8px] font-bold tracking-[0.2em] text-fws-dark uppercase border-r border-fws-green/10 align-middle whitespace-nowrap">
                  Best For
                </th>
                <td className="py-2 px-4 text-xs font-sans font-medium text-fws-grey tracking-tight align-middle">
                  {venue.tags.join(' & ')}
                </td>
              </tr>
              <tr className="hover:bg-fws-light/30 transition-colors">
                {/* Reduced padding in column 1 (th) using px-1 */}
                <th className="py-2 px-2 bg-fws-light text-[8px] font-bold tracking-[0.2em] text-fws-dark uppercase border-r border-fws-green/10 align-middle whitespace-nowrap">
                  Hire Price
                </th>
                <td className="py-2 px-4 text-xs font-sans font-bold text-fws-green align-middle">
                  {venue.price}
                </td>
              </tr>
              <tr className="hover:bg-fws-light/30 transition-colors">
                {/* Reduced padding in column 1 (th) using px-1 */}
                <th className="py-2 px-2 bg-fws-light text-[8px] font-bold tracking-[0.2em] text-fws-dark uppercase border-r border-fws-green/10 align-middle whitespace-nowrap">
                  Capacity
                </th>
                <td className="py-2 px-4 text-xs font-sans font-medium text-fws-grey align-middle">
                  {venue.capacity} guests
                </td>
              </tr>
              <tr className="hover:bg-fws-light/30 transition-colors">
                {/* Reduced padding in column 1 (th) using px-1 */}
                <th className="py-2 px-2 bg-fws-light text-[8px] font-bold tracking-[0.2em] text-fws-dark uppercase border-r border-fws-green/10 align-middle whitespace-nowrap">
                  Airport
                </th>
                <td className="py-2 px-4 text-xs font-sans font-medium text-fws-grey italic align-middle">
                  {venue.closestAirport}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* 5. CTA Links */}
      <div className="flex flex-wrap items-center gap-x-8 gap-y-3 pt-2">
        <button className="group text-fws-dark hover:text-fws-green transition-all duration-300 py-1 text-[10px] font-bold tracking-[0.2em] uppercase flex items-center gap-2 border-b border-transparent hover:border-fws-green/30">
          <svg className="w-3 h-3 transform group-hover:-translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" className="rotate-180 origin-center" />
          </svg>
          Explore {shortName}
        </button>
        
        <button className="group text-fws-grey hover:text-fws-green transition-all duration-300 py-1 text-[10px] font-bold tracking-[0.2em] uppercase flex items-center gap-2 border-b border-transparent hover:border-fws-green/30">
          <svg className="w-3 h-3 opacity-60 group-hover:opacity-100" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          {shortName} Review
        </button>
        
        <button className="group text-fws-dark hover:text-fws-green transition-all duration-300 py-1 text-[10px] font-bold tracking-[0.2em] uppercase flex items-center gap-2 border-b border-transparent hover:border-fws-green/30">
          <svg className="w-3 h-3 text-fws-green group-hover:scale-110 transition-transform" fill="currentColor" viewBox="0 0 24 24">
             <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
          </svg>
          {shortName} Real Wedding
        </button>
      </div>
    </div>
  );
};

export default VenueCard;