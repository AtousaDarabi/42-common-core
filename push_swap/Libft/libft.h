/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   libft.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jukohler <jukohler@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/23 20:07:45 by jukohler          #+#    #+#             */
/*   Updated: 2026/06/25 16:30:13 by jukohler         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef LIBFT_H
# define LIBFT_H

# include <stddef.h>
# include <unistd.h>

int		ft_atoi(char *str, int *error);
void	ft_bzero(void *s, size_t n);
void	*ft_memset(void *b, int c, size_t len);
void	ft_putstr_fd(char *s, int fd);
int		ft_strcmp(const char *s1, const char *s2);

#endif
