/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_helper.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/12 15:44:01 by adarabi           #+#    #+#             */
/*   Updated: 2026/05/28 21:22:58 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_print_char(char c)
{
	return (write(1, &c, 1));
}

int	ft_print_num(unsigned long nbr, char c)
{
	if (c == 'X')
		return (ft_print_number(c, nbr, "0123456789ABCDEF"));
	if (c == 'x')
		return (ft_print_number(c, nbr, "0123456789abcdef"));
	if (c == 'd' || c == 'i')
		return (ft_print_number(c, nbr, "0123456789"));
	if (c == 'u')
	{
		nbr = (unsigned long)(unsigned int)nbr;
		return (ft_print_number(c, nbr, "0123456789"));
	}
	return (0);
}

int	ft_print_number(char c, long l, char *arr)
{
	unsigned long	nbr;
	int				total;
	int				base;

	total = 0;
	base = ft_strlen(arr);
	if ((c == 'd' || c == 'i') && (int)l < 0)
	{
		total += write(1, "-", 1);
		nbr = (unsigned long)(-(long)(int)l);
	}
	else
		nbr = (unsigned long)l;
	if (nbr / base == 0)
		total += write(1, &arr[nbr % base], 1);
	else
	{
		total += ft_print_number(c, (long)(nbr / base), arr);
		total += write(1, &arr[nbr % base], 1);
	}
	return (total);
}

int	ft_print_pointer(void *ptr)
{
	int				total;
	unsigned long	ptrnbr;

	total = 0;
	ptrnbr = (unsigned long)ptr;
	if (ptrnbr == 0)
		total += write(1, "(nil)", 5);
	else
	{
		total += write(1, "0x", 2);
		total += ft_print_number('p', ptrnbr, "0123456789abcdef");
	}
	return (total);
}
