// Same format the backend uses, so a label looks identical everywhere.
export function citationLabel(filename, startLine, endLine) {
  if (startLine === endLine) return `${filename}, line ${startLine}`;
  return `${filename}, lines ${startLine}\u2013${endLine}`;
}

export const ACCESS_LEVELS = [
  { value: "public", label: "Public" },
  { value: "team", label: "Team" },
  { value: "lead_only", label: "Lead only" },
  { value: "restricted", label: "Restricted" },
];

export const accessLabel = (value) =>
  ACCESS_LEVELS.find((a) => a.value === value)?.label ?? value;
