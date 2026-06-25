/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/25 21:54:56 by adarabi           #+#    #+#             */
/*   Updated: 2026/06/25 21:54:59 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	put_str(const char *s)
{
	int	len;

	len = 0;
	if (!s)
		return (0);
	while (s[len])
	{
		write(2, &s[len], 1);
		len++;
	}
	return (len);
}

static int	put_int(int n)
{
	char	buf[12];
	int		i;
	long	nb;

	nb = n;
	i = 11;
	buf[i] = '\0';
	if (nb == 0)
		buf[--i] = '0';
	if (nb < 0)
		nb = -nb;
	while (nb > 0)
	{
		buf[--i] = '0' + (nb % 10);
		nb /= 10;
	}
	if (n < 0)
		buf[--i] = '-';
	return (put_str(&buf[i]));
}

static int	put_char(char c)
{
	write(2, &c, 1);
	return (1);
}

static int	handle_spec(const char *fmt, va_list *ap)
{
	if (*fmt == 'd' || *fmt == 'i')
		return (put_int(va_arg(*ap, int)));
	if (*fmt == 's')
		return (put_str(va_arg(*ap, char *)));
	if (*fmt == 'c')
		return (put_char((char)va_arg(*ap, int)));
	write(2, fmt, 1);
	return (1);
}

int	ft_printf(const char *fmt, ...)
{
	va_list	ap;
	int		ret;

	if (!fmt)
		return (-1);
	va_start(ap, fmt);
	ret = 0;
	while (*fmt)
	{
		if (*fmt == '%' && *(fmt + 1))
			ret += handle_spec(++fmt, &ap);
		else
		{
			write(2, fmt, 1);
			ret++;
		}
		fmt++;
	}
	va_end(ap);
	return (ret);
}
