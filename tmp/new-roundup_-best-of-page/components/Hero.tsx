import React from 'react';

const Hero: React.FC = () => {
  return (
    <div className="relative h-[80vh] min-h-[600px] w-full flex items-center justify-center overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center transition-transform duration-[20s] hover:scale-110"
        style={{ 
          backgroundImage: 'url("https://images.unsplash.com/photo-1510076857177-7470076d4098?q=80&w=2500&auto=format&fit=crop")',
        }}
      >
        <div className="absolute inset-0 bg-black/30"></div>
      </div>

      {/* Photo credit */}
      <span className="absolute bottom-4 right-4 text-[9px] uppercase tracking-[0.3em] text-white/30 pointer-events-none select-none z-10">
        Photo credit
      </span>

      {/* Content */}
      <div className="relative text-center px-4 max-w-4xl">
        <div className="flex items-center justify-center space-x-2 text-white text-[10px] tracking-widest mb-8 uppercase font-semibold">
          <a href="/" className="hover:text-fws-green transition-colors">Home</a>
          <span>/</span>
          <a href="/venues" className="hover:text-fws-green transition-colors">Wedding Venues</a>
          <span>/</span>
          <span className="text-white/60">South of France</span>
        </div>
        
        <h1 className="text-4xl md:text-6xl lg:text-7xl text-white font-serif mb-6 leading-tight">
          Wedding Venues in the South of France
        </h1>
        
        <div className="w-24 h-px bg-fws-green mx-auto mb-8"></div>
        
        <p className="text-white text-lg md:text-xl font-sans font-light tracking-wide max-w-2xl mx-auto italic">
          Curated collection of the most exquisite Châteaux, Villas, and Estates in the French Riviera and Provence.
        </p>
      </div>
      
      {/* Scroll Down Indicator */}
      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 animate-bounce">
        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </div>
    </div>
  );
};

export default Hero;