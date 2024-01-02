"use client";

import {useEffect, useRef} from "react";

type Callback = () => void;


export const useMount = (callback: Callback) => {
  const hasMounted = useRef<boolean>(false);

  useEffect(() => {
    if (hasMounted.current) {
      return;
    }

    hasMounted.current = true;
    callback();
  }, []);
}