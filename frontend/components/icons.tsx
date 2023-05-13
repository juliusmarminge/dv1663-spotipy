import { twMerge } from "tailwind-merge";

interface IconProps extends React.SVGProps<SVGSVGElement> {}

export function More(props: IconProps) {
  const { className, ...rest } = props;
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={twMerge("h-6 fill-current stroke-current", className)}
      {...rest}
    >
      <circle cx="12" cy="12" r="1"></circle>
      <circle cx="19" cy="12" r="1"></circle>
      <circle cx="5" cy="12" r="1"></circle>
    </svg>
  );
}

export function Home(props: IconProps) {
  const { className, ...rest } = props;
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={twMerge("h-6 fill-none stroke-current", className)}
      {...rest}
    >
      <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
      <polyline points="9 22 9 12 15 12 15 22"></polyline>
    </svg>
  );
}

export function Search(props: IconProps) {
  const { className, ...rest } = props;
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={twMerge("h-6 fill-none stroke-current", className)}
      {...rest}
    >
      <circle cx="11" cy="11" r="8"></circle>
      <line x1="21" x2="16.65" y1="21" y2="16.65"></line>
    </svg>
  );
}

export function Previous(props: IconProps) {
  const { className, ...rest } = props;
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={twMerge("h-6 fill-none stroke-current", className)}
      {...rest}
    >
      <polyline points="17 18 11 12 17 6"></polyline>
      <path d="M7 6v12"></path>
    </svg>
  );
}

export function Next(props: IconProps) {
  const { className, ...rest } = props;
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      strokeWidth={2}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={twMerge("h-6 fill-none stroke-current", className)}
      {...rest}
    >
      <polyline points="7 18 13 12 7 6"></polyline>
      <path d="M17 6v12"></path>
    </svg>
  );
}

export function Play(props: IconProps) {
  const { className, ...rest } = props;
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      strokeWidth={2}
      className={twMerge("h-6 fill-current stroke-current", className)}
      {...rest}
    >
      <polygon points="5 3 19 12 5 21 5 3"></polygon>
    </svg>
  );
}

export function Pause(props: IconProps) {
  const { className, ...rest } = props;
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      strokeWidth={3}
      className={twMerge("h-6 fill-none stroke-current", className)}
      {...rest}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15.75 5.25v13.5m-7.5-13.5v13.5"
      />
    </svg>
  );
}
