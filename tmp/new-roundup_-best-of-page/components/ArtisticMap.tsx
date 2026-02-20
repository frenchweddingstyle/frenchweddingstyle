import React from 'react';

const ArtisticMap: React.FC = () => {
  return (
    <div className="relative w-full max-w-5xl mx-auto py-16 px-4">
      <div className="text-center mb-12">
        <h2 className="text-4xl md:text-5xl lg:text-6xl text-fws-dark mb-4">A Geographic Glimpse</h2>
        <p className="text-fws-grey font-light max-w-2xl mx-auto text-sm italic">
          Discover the layout of the regions that define French destination luxury.
        </p>
      </div>

      <div className="relative bg-fws-light/40 border border-fws-green/10 rounded-2xl p-6 md:p-12 shadow-inner overflow-hidden">
        {/* Artistic SVG Background - Stylized South of France Coastline */}
        <div className="relative aspect-[16/10] w-full">
          <svg 
            viewBox="0 0 1000 600" 
            className="w-full h-full drop-shadow-sm opacity-20 pointer-events-none select-none"
            fill="none" 
            xmlns="http://www.w3.org/2000/svg"
          >
            {/* Coastline Sketch */}
            <path 
              d="M50,150 Q150,140 250,160 T450,180 T650,220 T850,280 L950,350 L950,550 L50,550 Z" 
              fill="#808254" 
              fillOpacity="0.05"
              stroke="#808254" 
              strokeWidth="1" 
              strokeDasharray="5 5"
            />
            {/* Sea Texture */}
            <path d="M700,450 Q750,440 800,450" stroke="#808254" strokeWidth="0.5" strokeOpacity="0.3" />
            <path d="M720,470 Q770,460 820,470" stroke="#808254" strokeWidth="0.5" strokeOpacity="0.3" />
            
            {/* Decorative Compass */}
            <g transform="translate(80, 480) scale(0.6)">
               <circle cx="50" cy="50" r="40" stroke="#808254" strokeWidth="0.5" strokeOpacity="0.5" />
               <path d="M50,10 L50,90 M10,50 L90,50" stroke="#808254" strokeWidth="0.5" />
               <text x="45" y="5" className="text-[12px] fill-fws-green font-serif italic">N</text>
            </g>
          </svg>

          {/* Markers & Labels */}
          {/* Provence / Luberon Area */}
          <div className="absolute top-[25%] left-[40%] group cursor-default">
            <div className="w-3 h-3 bg-fws-green rounded-full animate-pulse mb-2"></div>
            <div className="absolute top-4 -left-4 whitespace-nowrap">
              <span className="font-serif italic text-xl md:text-2xl text-fws-dark block">Luberon</span>
              <span className="text-[9px] uppercase tracking-widest text-fws-green font-bold">Lavender & Bastides</span>
            </div>
          </div>

          {/* Alpilles Area */}
          <div className="absolute top-[35%] left-[28%] group cursor-default">
            <div className="w-2 h-2 border border-fws-green rounded-full mb-1"></div>
            <div className="absolute top-3 -left-2 whitespace-nowrap">
              <span className="font-serif italic text-lg md:text-xl text-fws-dark block">Les Alpilles</span>
              <span className="text-[8px] uppercase tracking-widest text-fws-grey">Historic Estates</span>
            </div>
          </div>

          {/* Marseille / Cassis */}
          <div className="absolute top-[48%] left-[32%] group cursor-default">
             <div className="w-2 h-2 bg-fws-dark/20 rounded-full mb-1"></div>
             <div className="absolute top-2 left-4 whitespace-nowrap">
                <span className="font-serif italic text-base text-fws-grey block">Cassis</span>
                <span className="text-[8px] uppercase tracking-widest text-fws-green">The Calanques</span>
             </div>
          </div>

          {/* French Riviera / Côte d'Azur */}
          <div className="absolute top-[40%] left-[75%] group cursor-default">
            <div className="w-3 h-3 bg-fws-green rounded-full animate-pulse mb-2"></div>
            <div className="absolute top-4 -left-10 whitespace-nowrap text-right">
              <span className="font-serif italic text-xl md:text-2xl text-fws-dark block">French Riviera</span>
              <span className="text-[9px] uppercase tracking-widest text-fws-green font-bold">Glamour & Sea Views</span>
            </div>
          </div>

          {/* Nice / Cap-Ferrat */}
          <div className="absolute top-[35%] left-[85%] group cursor-default">
            <div className="w-2 h-2 border border-fws-green rounded-full mb-1"></div>
            <div className="absolute top-3 -left-8 whitespace-nowrap">
              <span className="font-serif italic text-base text-fws-grey block">Cap-Ferrat</span>
            </div>
          </div>

          {/* Major City References */}
          <div className="absolute top-[38%] left-[10%] text-fws-grey/40 font-serif italic text-lg opacity-50 select-none">Occitanie →</div>
          <div className="absolute bottom-[15%] right-[10%] text-fws-grey/40 font-serif italic text-lg opacity-50 select-none pointer-events-none">Mediterranean Sea</div>
        </div>

        {/* Legend / Key */}
        <div className="mt-8 flex flex-wrap justify-center gap-8 border-t border-fws-green/10 pt-8">
           <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-fws-green rounded-full"></div>
              <span className="text-[9px] uppercase tracking-[0.2em] font-bold text-fws-dark">Major Region</span>
           </div>
           <div className="flex items-center gap-2">
              <div className="w-2 h-2 border border-fws-green rounded-full"></div>
              <span className="text-[9px] uppercase tracking-[0.2em] font-bold text-fws-dark">Key Location</span>
           </div>
           <div className="flex items-center gap-2">
              <div className="w-4 h-px bg-fws-green/30 border-t border-dashed"></div>
              <span className="text-[9px] uppercase tracking-[0.2em] font-bold text-fws-dark">Costal Flow</span>
           </div>
        </div>
      </div>
    </div>
  );
};

export default ArtisticMap;