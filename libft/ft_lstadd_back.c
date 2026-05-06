/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_back.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/04/30 14:10:51 by adarabi           #+#    #+#             */
/*   Updated: 2026/04/30 14:33:44 by adarabi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstadd_back(t_list **lst, t_list *new)
{
	t_list	*last;

	if (!lst || !new)
		return ;
	if (*lst == NULL)
	{
		*lst = new;
		return ;
	}
	last = ft_lstlast(*lst);
	last->next = new;
}

// int	main(void)
// {
// 	t_list	*head;
// 	t_list	*last;

// 	head = NULL;
// 	ft_lstadd_back(&head, ft_lstnew("Node 1"));
// 	ft_lstadd_back(&head, ft_lstnew("Node 2"));
// 	ft_lstadd_back(&head, ft_lstnew("Node 3"));
// 	last = ft_lstlast(head);
// 	printf("Last node is now: %s\n", (char *)last->content);
// 	return (0);
// }
