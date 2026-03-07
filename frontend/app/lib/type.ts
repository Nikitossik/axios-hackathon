export type UserEntity = {
  id: string;
  name: string;
  surname: string;
  email: string;
};
export type PaginatedUsers = {
  page: number;
  page_size: number;
  total: number;
  items: UserEntity[];
};
export interface AuthState {
  user: UserEntity | null;
  isLoading: boolean;
  error: string | null;
  isAuthenticated: boolean;
}

export interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  refreshAuth: () => Promise<void>;
}
