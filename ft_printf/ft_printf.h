/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/09 03:42:50 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/28 21:00:34 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H
# include <stddef.h>
# include <stdarg.h>
# include <unistd.h>
# include "libft/libft.h"

int	ft_printf(const char *str, ...);
int	ft_print_char(char c);
int	ft_print_num(unsigned long nbr, char c);
int	ft_print_number(char c, long l, char *arr);
int	ft_print_pointer(void *ptr);

#endif