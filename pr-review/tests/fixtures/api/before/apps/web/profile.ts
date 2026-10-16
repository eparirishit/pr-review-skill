export function label(user: {id: number; display_name: string}) {
  return user.display_name.toUpperCase();
}
