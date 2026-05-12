/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/08 15:27:01 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/12 23:20:52 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static	int	ft_print_conversion(char c, va_list arg_list)
{
	char	*str;
	int		sum;

	if (c == 'a')
		sum = write(1, "predefined text", 15);
	if (c == 'c')
		sum = ft_print_char(va_arg(arg_list, int));
	if (c == 's')
	{
		str = va_arg(arg_list, char *);
		if (str == NULL)
			sum = write(1, "(null)", 6);
		else
			sum = write(1, str, ft_strlen(str));
	}
	if (c == 'x' || c == 'X')
		sum = ft_print_hex(va_arg(arg_list, unsigned int), c);
	if (c == 'd' || c == 'i')
    	sum = ft_print_number(c, va_arg(arg_list, int), "0123456789");
	if (c == 'u')
		sum = ft_print_number(c, (long)va_arg(arg_list, unsigned int), "0123456789");
	if (c == 'p')
		sum = ft_print_pointer(va_arg(arg_list, void *));
	if (c == '%')
		sum = write(1, "%", 1);
	return (sum);
}

int	ft_printf(const char *str, ...)
{
	va_list	ap;
	int		total;
	int		i;

	total = 0;
	i = 0;
	if (str)
	{
		va_start(ap, str);
		while (*(str + i))
		{
			if (*(str + i) == '%')
			{
				total += ft_print_conversion((char)*(str + (i + 1)), ap);
				i++;
			}
			else
			{
				total += write(1, str + i, 1);
			}
			i++;
		}
		va_end(ap);
	}
	return (total);
}
