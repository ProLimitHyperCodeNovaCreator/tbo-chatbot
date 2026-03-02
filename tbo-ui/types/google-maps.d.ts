declare namespace google {
  namespace maps {
    class Map {
      constructor(container: HTMLElement, options: MapOptions);
      setCenter(latlng: LatLngLiteral | LatLng): void;
      setZoom(zoom: number): void;
      fitBounds(bounds: LatLngBounds, padding?: number): void;
    }

    interface MapOptions {
      zoom?: number;
      center?: LatLngLiteral | LatLng;
      mapTypeControl?: boolean;
      fullscreenControl?: boolean;
      zoomControl?: boolean;
      streetViewControl?: boolean;
      scrollwheel?: boolean;
      disableDoubleClickZoom?: boolean;
      styles?: MapTypeStyle[];
    }

    interface MapTypeStyle {
      featureType?: string;
      elementType?: string;
      stylers?: Array<{ [key: string]: string }>;
    }

    interface LatLngLiteral {
      lat: number;
      lng: number;
    }

    class LatLng {
      constructor(lat: number, lng: number);
      lat(): number;
      lng(): number;
    }

    class LatLngBounds {
      constructor(sw?: LatLng, ne?: LatLng);
      contains(latLng: LatLng | LatLngLiteral): boolean;
      equals(other: LatLngBounds): boolean;
      extend(point: LatLng | LatLngLiteral): LatLngBounds;
      getNorthEast(): LatLng;
      getSouthWest(): LatLng;
      intersects(other: LatLngBounds): boolean;
      isEmpty(): boolean;
      toSpan(): LatLng;
      toString(): string;
      toUrlValue(precision?: number): string;
    }

    class Marker {
      constructor(options: MarkerOptions);
      getMap(): Map | null;
      setMap(map: Map | null): void;
      setPosition(latlng: LatLng | LatLngLiteral): void;
      getPosition(): LatLng | null;
      setTitle(title: string): void;
      getTitle(): string;
      setIcon(icon: string | Icon | Symbol): void;
      addListener(eventName: string, callback: () => void): void;
    }

    interface MarkerOptions {
      position?: LatLngLiteral | LatLng;
      map?: Map;
      title?: string;
      icon?: string | Icon | Symbol;
      visible?: boolean;
      opacity?: number;
      clickable?: boolean;
      draggable?: boolean;
      animation?: Animation;
    }

    interface Icon {
      url: string;
      size?: Size;
      origin?: Point;
      anchor?: Point;
      scaledSize?: Size;
    }

    interface Symbol {
      path: string | SymbolPath;
      fillColor?: string;
      fillOpacity?: number;
      scale?: number;
      strokeColor?: string;
      strokeWeight?: number;
      rotation?: number;
    }

    enum SymbolPath {
      CIRCLE = 'circle',
      FORWARD_CLOSED_ARROW = 'forward_closed_arrow',
      FORWARD_OPEN_ARROW = 'forward_open_arrow',
      BACKWARD_CLOSED_ARROW = 'backward_closed_arrow',
      BACKWARD_OPEN_ARROW = 'backward_open_arrow',
    }

    enum Animation {
      BOUNCE = 1,
      DROP = 2,
    }

    class Size {
      constructor(width: number, height: number, widthUnits?: string, heightUnits?: string);
      equals(other: Size): boolean;
      toString(): string;
    }

    class Point {
      constructor(x: number, y: number);
      equals(other: Point): boolean;
      toString(): string;
    }

    class InfoWindow {
      constructor(options?: InfoWindowOptions);
      close(): void;
      getContent(): string | Element | null;
      getPosition(): LatLng | null;
      getZIndex(): number;
      open(map?: Map | null, anchor?: Marker | null): void;
      setContent(content: string | Element): void;
      setPosition(position: LatLng | LatLngLiteral): void;
      setZIndex(zIndex: number): void;
      addListener(eventName: string, callback: () => void): void;
    }

    interface InfoWindowOptions {
      content?: string | Element;
      disableAutoPan?: boolean;
      maxWidth?: number;
      pixelOffset?: Size;
      position?: LatLng | LatLngLiteral;
      zIndex?: number;
    }
  }
}

interface Window {
  google: typeof google;
}
