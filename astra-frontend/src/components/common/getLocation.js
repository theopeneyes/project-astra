export const getLocation = (pathname, pageName) => {
  const segments = pathname.split("/").filter(Boolean);
  if (pageName === "Header") {
    return segments[segments.length - 1];
  } else {
    return segments
  }
};
