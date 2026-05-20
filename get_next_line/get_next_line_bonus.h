/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_bonus.h                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/20 22:30:25 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/20 22:32:41 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef GET_NEXT_LINE_BONUS_H
# define GET_NEXT_LINE_BONUS_H

# include <unistd.h>
# include <stdlib.h>
# include <string.h>

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 42
# endif

char	*alloc_after(char *s, int idx);
char	*do_read(int fd, char **s, char *buff, size_t *len);
size_t	ft_strlen(char *str);
int		ft_chrfind(char *str, int c);
char	*get_next_line(int fd);
char	*ft_strjoin(char *s1, size_t len_s1, char *s2, size_t len_s2);
char	*fileread(int fd, char *s);
char	*get_first_line(char *s);

#endif
